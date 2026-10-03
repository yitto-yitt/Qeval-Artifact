# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import QProg, I, X, H


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    circuit = QProg()
    for i in range(num_qubits):
        circuit << I(i)
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(i)
        if basis[i] == 1:
            circuit << H(i)
    return circuit
