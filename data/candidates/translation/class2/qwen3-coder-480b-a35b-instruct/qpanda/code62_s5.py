# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import *

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(num_qubits)
    c = qvm.cAlloc_many(num_qubits)
    
    prog = QProg()
    
    for i in range(len(basis)):
        if state[i] == 1:
            prog << X(q[i])
        if basis[i] == 1:
            prog << H(q[i])
    
    finalize()
    return prog
