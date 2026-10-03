# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import QProg, X, H, qAlloc_many

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qubits = qAlloc_many(num_qubits)
    circuit = QProg()
    for i in range(num_qubits):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    return circuit
