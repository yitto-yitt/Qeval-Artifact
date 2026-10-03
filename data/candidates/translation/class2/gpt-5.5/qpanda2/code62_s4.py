# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, X, H


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QProg()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(H(qubits[i]))

    if not hasattr(bb84_senders_circuit, "_resources"):
        bb84_senders_circuit._resources = []
    bb84_senders_circuit._resources.append((qvm, qubits))

    return circuit
