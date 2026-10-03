# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def create_quantum_circuit(n_qubits):
    prog = QProg()
    for i in range(n_qubits):
        prog << I(qubits[i])
    return prog

machine.finalize()
