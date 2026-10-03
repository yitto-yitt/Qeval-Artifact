# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        oracle_qubits = sorted(oracle.all_qubits())
        n = len(oracle_qubits)
        qubits = oracle_qubits
    else:
        raise ValueError("Oracle must be a cirq.Circuit")

    input_qubits = qubits[:n - 1]
    output_qubit = qubits[n - 1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H(q) for q in qubits)
    circuit += oracle
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*input_qubits, key='c'))

    simulator = cirq.Simulator()
    repetitions = 4096
    result = simulator.run(circuit, repetitions=repetitions)

    measurements = result.measurements['c']
    counts = {}
    for shot in measurements:
        bitstring = ''.join(str(int(b)) for b in shot[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
