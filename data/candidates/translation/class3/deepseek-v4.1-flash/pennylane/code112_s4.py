# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            pauli_op = qml.pauli.string_to_pauli_word(pauli_string)
            hamiltonian = qml.Hamiltonian([1.0], [pauli_op])
            qml.TrotterProduct(hamiltonian, time, n=reps, order=1)
        return qml.state()
    
    return circuit
