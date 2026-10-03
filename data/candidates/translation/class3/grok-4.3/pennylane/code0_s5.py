# EVAL_META: task_id=0, framework=pennylane, class=3
import pennylane as qml
def create_quantum_circuit(n_qubits):
    return qml.device("default.qubit", wires=n_qubits)
