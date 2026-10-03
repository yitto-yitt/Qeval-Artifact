# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for k in range(8):
        qubit_idx = 7 - k
        if (a >> k) & 1:
            circuit.append(cirq.X(qubits[qubit_idx]))
        if (b >> k) & 1:
            circuit.append(cirq.X(qubits[qubit_idx]))
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    bits = result.measurements['result']
    def to_str(row):
        return ''.join(map(str, row))
    counts = Counter(to_str(row) for row in bits)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
