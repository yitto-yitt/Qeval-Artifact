# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Get target unitary from the input circuit
    target_matrix = qml.matrix(circuit)()
    dim = target_matrix.shape[0]
    num_qubits = int(np.log2(dim))

    # Equivalence check up to global phase
    def are_equiv(U1, U2, rtol=0.4, atol=0.4):
        inner = np.sum(np.conj(U1) * U2)
        mag = np.abs(inner)
        if mag == 0:
            return False
        phase = inner / mag
        return np.allclose(U1, U2 * phase, rtol=rtol, atol=atol)

    qc_list = []
    counter = 0
    dev = qml.device('default.qubit', wires=num_qubits)

    while counter < n:
        # Build a random Clifford circuit as a QNode
        @qml.qnode(dev)
        def candidate():
            depth = 10 * num_qubits
            for _ in range(depth):
                if np.random.random() < 0.4:
                    qubit = np.random.randint(0, num_qubits)
                    gate = np.random.choice(['H', 'S', 'X', 'Y', 'Z'])
                    if gate == 'H':
                        qml.Hadamard(wires=qubit)
                    elif gate == 'S':
                        qml.S(wires=qubit)
                    elif gate == 'X':
                        qml.PauliX(wires=qubit)
                    elif gate == 'Y':
                        qml.PauliY(wires=qubit)
                    elif gate == 'Z':
                        qml.PauliZ(wires=qubit)
                else:
                    if num_qubits >= 2:
                        control, target = np.random.choice(num_qubits, size=2, replace=False)
                        qml.CNOT(wires=[control, target])
            return qml.state()
        cand_matrix = qml.matrix(candidate)()
        if are_equiv(target_matrix, cand_matrix):
            counter += 1
            qc_list.append(candidate)

    return qc_list
