# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import QCircuit, qAlloc_many, X, H, init, QMachineType


def bb84_senders_circuit(state, basis):
    init(QMachineType.CPU)
    qubits = qAlloc_many(len(state))
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    return circuit
