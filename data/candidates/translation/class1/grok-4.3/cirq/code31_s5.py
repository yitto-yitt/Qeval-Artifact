# EVAL_META: task_id=31, framework=cirq, class=1
import cirq
from typing import Dict

def sampler_qiskit():
    qubits = cirq.LineQubit.range(2)
    qc = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(qubits[0], qubits[1], key='meas')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(qc, repetitions=1024)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
