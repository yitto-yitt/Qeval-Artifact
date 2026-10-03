# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    ops = []
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            theta = 2 * (time / reps)
            op = qml.PauliRot(theta, pauli_string, wires=range(n_qubits))
            ops.append(op)
    return QuantumScript(ops)
