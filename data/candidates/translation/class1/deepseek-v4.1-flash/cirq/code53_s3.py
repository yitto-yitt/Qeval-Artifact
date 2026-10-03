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
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['result']
    bitstrings = []
    for row in measurements:
        bitstring = ''.join(str(row[i]) for i in range(7, -1, -1))
        bitstrings.append(bitstring)
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
