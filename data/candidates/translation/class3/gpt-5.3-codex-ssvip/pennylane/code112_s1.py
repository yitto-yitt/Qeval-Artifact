# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        wire_order = list(range(n_qubits))
        for pauli_string, time in zip(pauli_strings, times):
            coeffs = [1.0]
            ops = [qml.pauli.string_to_pauli_word(pauli_string, wire_map={i: i for i in range(n_qubits)})]
            qml.TrotterProduct(qml.Hamiltonian(coeffs, ops), time=float(time), order=int(order), n=int(reps))
        return qml.state()

    circuit()
    return circuit
