# EVAL_META: task_id=31, framework=cirq, class=1
import cirq
from typing import Dict

def sampler_qiskit():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(*qubits, key='result'))
    
    simulator = cirq.Simulator(seed=42)
    results = simulator.run(circuit, repetitions=1000)
    measurements = results.measurements['result']
    
    counts = {}
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
