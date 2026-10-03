# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit() -> Dict[str, float]:
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.measure(*qubits, key='m')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = {}
    for row in result.measurements['m']:
        bitstring = ''.join(str(int(b)) for b in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
