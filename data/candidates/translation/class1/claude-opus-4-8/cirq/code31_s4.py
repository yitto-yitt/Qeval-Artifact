# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.measure(*q, key='meas'))

    sim = cirq.Simulator(seed=42)
    result = sim.run(circuit, repetitions=1024)
    counts = result.histogram(key='meas')

    total = sum(counts.values())
    dist = {}
    for value, count in counts.items():
        bitstring = format(value, '02b')
        dist[bitstring] = count / total
    return dist
