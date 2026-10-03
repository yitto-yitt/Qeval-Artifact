# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda import *
from pyqpanda.core import *


def compose_cnot_dihedral():
    # Create first quantum circuit
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog1 = QProg()
    prog1.insert(CNOT(qubits[0], qubits[1]))
    prog1.insert(T(qubits[0]))
    
    # Create second quantum circuit
    prog2 = QProg()
    prog2.insert(CNOT(qubits[0], qubits[1]))
    prog2.insert(T(qubits[0]))
    prog2.insert(X(qubits[1]))
    
    # Convert to CNOTDihedral elements and compose
    # In pyQPanda, we need to use the underlying quantum operations directly
    # Since there's no direct CNOTDihedral class, we'll return the composed program
    composed_prog = QProg()
    composed_prog.insert(prog1)
    composed_prog.insert(prog2)
    
    qvm.finalize()
    return composed_prog
