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
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*input_qubits, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    counts = result.histogram(key='result')
    
    total = sum(counts.values())
    bitstrings = {}
    for k, v in counts.items():
        bitstring = format(k, f'0{n-1}b')
        bitstrings[bitstring] = v / total
    
    return bitstrings
