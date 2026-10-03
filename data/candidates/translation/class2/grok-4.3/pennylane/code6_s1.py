# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml

def create_state_prep(num_qubits):
    def circuit():
        qml.BasisState([(1 >> i) & 1 for i in range(num_qubits)], wires=range(num_qubits))
    return circuit
