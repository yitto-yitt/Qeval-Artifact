# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit)
    num_qubits = circuit.num_wires
    qc_list = []
    counter = 0
    while counter < n:
        with qml.tape.QuantumTape() as qc:
            for _ in range(np.random.randint(2 * num_qubits, 5 * num_qubits)):
                gate_choice = np.random.choice([0, 1, 2])
                if gate_choice == 0:
                    qml.Hadamard(wires=int(np.random.randint(num_qubits)))
                elif gate_choice == 1:
                    qml.S(wires=int(np.random.randint(num_qubits)))
                else:
                    w = np.random.choice(num_qubits, 2, replace=False)
                    qml.CNOT(wires=[int(w[0]), int(w[1])])
        op_qc = qml.matrix(qc)
        prod = op_qc @ np.conjugate(op_or).T
        if np.allclose(prod, prod[0, 0] * np.eye(2 ** num_qubits), rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
