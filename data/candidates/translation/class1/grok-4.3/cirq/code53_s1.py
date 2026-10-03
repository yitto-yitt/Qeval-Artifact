# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
from collections import Counter

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for i in range(8):
        bit_val = 1 << (7 - i)
        if a & bit_val:
            circuit.append(cirq.X(qubits[i]))
        if b & bit_val:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    simulator = cirq.Simulator()
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)
    samples = result.measurements['meas']
    bitstrings = [''.join(map(str, sample)) for sample in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
