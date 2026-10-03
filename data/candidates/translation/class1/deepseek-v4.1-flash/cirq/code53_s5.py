# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    n = 8
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for i in range(n):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(n):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*reversed(qubits), key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['m']
    bitstrings = [''.join(str(int(bit)) for bit in row) for row in measurements]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
