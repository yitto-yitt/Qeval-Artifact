# EVAL_META: task_id=55, framework=cirq, class=1
import cirq
from collections import Counter

def or_gate(a: int, b: int):
    qr_a = cirq.LineQubit.range(0, 3)
    qr_b = cirq.LineQubit.range(3, 6)
    ancillary = cirq.LineQubit.range(6, 9)
    
    circuit = cirq.Circuit()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            circuit.append(cirq.X(qr_a[i]))
        if b_str[2-i] == '0':
            circuit.append(cirq.X(qr_b[i]))
            
    for i in range(3):
        circuit.append(cirq.CCNOT(qr_a[i], qr_b[i], ancillary[i]))
        
    for i in range(3):
        circuit.append(cirq.X(ancillary[i]))
        
    circuit.append(cirq.measure(ancillary[2], ancillary[1], ancillary[0], key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    measurements = result.measurements['result']
    counts = Counter()
    for row in measurements:
        bitstring = "".join(str(bit) for bit in row)
        counts[bitstring] += 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
