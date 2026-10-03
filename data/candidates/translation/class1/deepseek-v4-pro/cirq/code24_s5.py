# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.qubits)
    qubits = oracle.qubits
    data_qubits = qubits[:-1]
    ancilla = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(ancilla))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle)
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*data_qubits, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=5000)
    counts = result.histogram(key='result')

    total = sum(counts.values())
    distribution = {}
    for k, v in counts.items():
        bitstring = format(k, f'0{n-1}b')
        distribution[bitstring] = v / total
    return distribution
