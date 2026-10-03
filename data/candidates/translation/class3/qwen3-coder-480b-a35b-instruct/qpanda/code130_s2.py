# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    machine = init_quantum_machine(QMachineType.CPU)
    qvec = machine.qAlloc_many(n)
    prog = QProg()
    
    # Apply Hadamard gates to the second and third qubits (indices 1 and 2)
    for i in range(2):
        prog.insert(H(qvec[i+1]))
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    for i in range(2):
        prog.insert(CNOT(qvec[i+1], qvec[i+2+1]))
    
    # Get the inverse of the program
    inv_prog = get_inverse(prog)
    
    return inv_prog
