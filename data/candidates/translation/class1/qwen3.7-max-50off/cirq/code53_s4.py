# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    circuit.append(cirq.measure(*qubits[::-1], key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['m']
    str_counts = Counter(''.join(map(str, row)) for row in measurements)
    total = sum(str_counts.values())
    
    return {k: v / total for k, v in str_counts.items()}
