# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X, H, qAlloc, init

def bb84_senders_circuit(state, basis):
    init()
    qubits = qAlloc(len(state))
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(H(qubits[i]))
    return circuit
