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

    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    n_input = len(input_qubits)
    prob_dist = {}
    for bit_val, count in counts.items():
        bitstring = format(bit_val, f'0{n_input}b')
        prob_dist[bitstring] = count / total
    return prob_dist
