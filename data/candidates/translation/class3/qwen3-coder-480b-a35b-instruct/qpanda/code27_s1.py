# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda import *
from pyqpanda.core import *


def apply_op_back():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    
    # Apply Hadamard operation to the back of qubit 0
    prog.insert(H(qubits[0]))
    
    return prog
