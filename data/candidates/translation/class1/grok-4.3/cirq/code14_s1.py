# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=10)
    samples = result.measurements['meas']
    bitstrings = [''.join(str(bit) for bit in sample) for sample in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
