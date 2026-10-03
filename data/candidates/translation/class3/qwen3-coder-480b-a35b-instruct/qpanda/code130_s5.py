# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    machine = CPUQVM()
    machine.init_qvm()
    qv = machine.qAlloc_many(n)
    
    prog = QProg()
    
    # Apply Hadamard gates to the second and third qubits (indices 1 and 2)
    for i in range(2):
        prog.insert(H(qv[i + 1]))
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    for i in range(2):
        prog.insert(CNOT(qv[i + 1], qv[i + 2 + 1]))
    
    # Get the inverse of the program
    inv_prog = prog.dagger()
    
    machine.finalize()
    
    return inv_prog
