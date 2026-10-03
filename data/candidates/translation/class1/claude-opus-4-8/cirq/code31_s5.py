# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CX(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='meas'))

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)

    measurements = result.measurements['meas']
    counts: Dict[str, int] = {}
    for shot in measurements:
        bitstring = ''.join(str(int(b)) for b in shot)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
