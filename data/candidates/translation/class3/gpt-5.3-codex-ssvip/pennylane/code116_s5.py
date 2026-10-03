# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    wire_map = list(range(n_qubits))
    op_map = {"I": qml.Identity, "X": qml.PauliX, "Y": qml.PauliY, "Z": qml.PauliZ}

    ops = [op_map[p](wire_map[i]) for i, p in enumerate(pauli_string)]
    pauli_op = ops[0]
    for op in ops[1:]:
        pauli_op = pauli_op @ op

    H = qml.Hamiltonian([1.0], [pauli_op])
    U = qml.matrix(qml.evolve(H)(time), wire_order=wire_map)

    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=wire_map)
        return qml.state()

    return circuit
