# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
from collections import Counter

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements['m']
    
    counts = Counter()
    for row in measurements:
        key = "".join(str(bit) for bit in reversed(row))
        counts[key] += 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
