# EVAL_META: task_id=24, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    total_qubits = oracle.num_qubits
    n_input = total_qubits - 1

    q = QuantumRegister(total_qubits, 'q')
    c = ClassicalRegister(n_input, 'c')
    qc = QuantumCircuit(q, c)

    all_qubits = [q[i] for i in range(total_qubits)]
    input_qubits = [q[i] for i in range(n_input)]
    output_qubit = q[n_input]

    qc.x(output_qubit)
    qc.h(all_qubits)
    qc.append(oracle, all_qubits)
    qc.h(input_qubits)
    qc.measure(input_qubits, c)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)

    total_shots = sum(counts.values())
    return {bitstring: count / total_shots for bitstring, count in counts.items()}
