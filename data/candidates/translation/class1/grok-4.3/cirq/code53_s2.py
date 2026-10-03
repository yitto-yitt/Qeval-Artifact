# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    simulator = cirq.Simulator()
    samples = simulator.run(circuit, repetitions=1024)
    meas = samples.measurements['meas']
    bitstrings = [''.join(map(str, row[::-1])) for row in meas]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
