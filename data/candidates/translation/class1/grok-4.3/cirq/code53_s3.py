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
    results = simulator.run(circuit, repetitions=1024)
    meas_data = results.measurements['result']
    bitstrings = [''.join(map(str, row[::-1])) for row in meas_data]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
