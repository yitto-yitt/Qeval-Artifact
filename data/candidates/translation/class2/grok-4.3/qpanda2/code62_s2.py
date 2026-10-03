# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import *

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = CPUQVM()
    machine.init_qvm()
    qprog = QProg()
    qubits = machine.qAlloc_many(num_qubits)
    for i in range(len(basis)):
        if state[i] == 1:
            qprog << X(qubits[i])
        if basis[i] == 1:
            qprog << H(qubits[i])
    return qprog
