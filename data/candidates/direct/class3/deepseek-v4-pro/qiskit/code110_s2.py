# EVAL_META: task_id=110, framework=qiskit, class=3

from qiskit.quantum_info import random_clifford

def equivalent_clifford_circuit(circuit, n):
    circuits = []
    for _ in range(n):
        qc = circuit.copy()
        random_c = random_clifford(qc.num_qubits)
        random_qc = random_c.to_circuit()
        qubits = list(qc.qubits)

        qc.compose(random_qc, qubits=qubits, inplace=True)
        qc.compose(random_qc.inverse(), qubits=qubits, inplace=True)

        circuits.append(qc)

    return circuits
