# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import QCircuit, X, H, Qubit


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(num_qubits)]
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    return circuit
