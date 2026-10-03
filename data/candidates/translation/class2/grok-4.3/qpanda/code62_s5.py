# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import qAlloc_many, QCircuit, X, H


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qubits = qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    return circuit
