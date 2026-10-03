# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    dev = qml.device('default.qubit', wires=num_qubits)
    @qml.qnode(dev)
    def circuit():
        qml.adjoint(qml.QFT)(wires=range(num_qubits))
        return qml.state()
    return circuit
