# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit)
    num_qubits = len(circuit.wires)
    qc_list = []
    counter = 0
    while counter < n:
        with qml.tape.QuantumTape() as qc:
            for _ in range(np.random.randint(5, 20)):
                gate_choice = np.random.choice(["H", "S", "CNOT"])
                if gate_choice == "H":
                    q = np.random.randint(0, num_qubits)
                    qml.Hadamard(wires=q)
                elif gate_choice == "S":
                    q = np.random.randint(0, num_qubits)
                    qml.S(wires=q)
                elif gate_choice == "CNOT":
                    q1 = np.random.randint(0, num_qubits)
                    q2 = np.random.randint(0, num_qubits)
                    while q2 == q1:
                        q2 = np.random.randint(0, num_qubits)
                    qml.CNOT(wires=[q1, q2])
        op_qc = qml.matrix(qc)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
