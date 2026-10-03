# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import QProg, QCircuit, H, X


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(i)
        if basis[i] == 1:
            circuit << H(i)
    return circuit
