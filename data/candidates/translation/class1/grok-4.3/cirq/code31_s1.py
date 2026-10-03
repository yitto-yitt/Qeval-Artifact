# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CX(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='meas')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {format(key, '02b'): value / total for key, value in counts.items()}
