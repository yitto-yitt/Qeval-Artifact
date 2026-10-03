# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, CNOT, T, X
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    # Create first quantum program
    prog1 = QProg()
    prog1.insert(CNOT(qubits[0], qubits[1]))
    prog1.insert(T(qubits[0]))
    
    # Create second quantum program (same as first with additional X gate)
    prog2 = QProg()
    prog2.insert(CNOT(qubits[0], qubits[1]))
    prog2.insert(T(qubits[0]))
    prog2.insert(X(qubits[1]))
    
    # Convert programs to unitary matrices for representation
    unitary1 = pq.get_unitary(prog1, machine)
    unitary2 = pq.get_unitary(prog2, machine)
    
    # Compose the operations by matrix multiplication
    composed_unitary = np.dot(unitary2, unitary1)
    
    # Return the composed program
    composed_prog = prog1 + prog2
    return composed_prog

result = compose_cnot_dihedral()
machine.finalize()
