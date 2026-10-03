# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    # Create first circuit: CX on qubits 0,1 and T on qubit 0
    prog1 = pq.QProg()
    prog1 << CNOT(qubits[0], qubits[1]) << T(qubits[0])
    
    # Create second circuit: same as first but with X on qubit 1
    prog2 = pq.QProg()
    prog2 << CNOT(qubits[0], qubits[1]) << T(qubits[0]) << X(qubits[1])
    
    # Convert to CNOTDihedral-like objects (using QProg as representation)
    # In pyqpanda we work directly with programs
    composed_prog = prog1 + prog2
    
    return composed_prog

machine.finalize()
