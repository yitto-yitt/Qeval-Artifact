# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, X, H

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAlloc(num_qubits)
    circ = QCircuit()
    for i in range(len(basis)):
        if int(state[i]) == 1:
            circ << X(qubits[i])
        if int(basis[i]) == 1:
            circ << H(qubits[i])
    return circ
