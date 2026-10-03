# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit(n_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n_qubits)
    prog = QProg()
    return prog
