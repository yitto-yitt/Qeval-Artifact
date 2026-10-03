# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.qubits)
    qubits = oracle.qubits
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle)
    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append(cirq.measure(*input_qubits, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')

    total = 1024
    n_input = len(input_qubits)
    distribution = {}
    for i in range(2**n_input):
        bitstring = format(i, f'0{n_input}b')
        distribution[bitstring] = counts.get(i, 0) / total

    return distribution
