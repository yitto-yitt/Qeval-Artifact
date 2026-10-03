# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
from collections import Counter

def run_bell_state_simulator():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(qubits[0], qubits[1], key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    samples = result.measurements['meas']
    bitstrings = [''.join(map(str, sample)) for sample in samples]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
