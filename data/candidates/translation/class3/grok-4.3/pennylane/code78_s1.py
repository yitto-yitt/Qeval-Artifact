# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    return qml.adjoint(qml.QFT(wires=range(num_qubits)))
