# EVAL_META: task_id=54, framework=cirq, class=1
import cirq
from collections import Counter

def and_gate(a, b):
    qr_a = cirq.LineQubit.range(0, 3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2-i] == '1':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.CCX(qr_a[i], qr_b[i], ancillary[i]))
        
    circuit.append(cirq.measure(*ancillary, key='measure'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements['measure']
    
    bitstrings = []
    for shot in measurements:
        s = f"{shot[2]}{shot[1]}{shot[0]}"
        bitstrings.append(s)
        
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
