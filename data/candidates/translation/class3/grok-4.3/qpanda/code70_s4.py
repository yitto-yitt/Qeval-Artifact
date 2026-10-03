# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = QProg()
    prog << H(qubits[0])
    prog << CSWAP(qubits[0], qubits[1], qubits[2])
    prog << H(qubits[1])
    prog << CSDG(qubits[1], qubits[0])
    return prog
