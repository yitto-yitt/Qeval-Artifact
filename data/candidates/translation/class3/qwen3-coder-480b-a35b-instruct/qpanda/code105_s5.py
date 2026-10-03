# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def initialize_cnot_dihedral():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.CX(qubits[0], qubits[1]))
    prog.insert(pq.T(qubits[0]))
    
    # In pyQPanda3, we work directly with the quantum program
    # since there isn't a direct equivalent to Qiskit's CNOTDihedral
    pq.directly_run(prog)
    
    # Return the program as the representation of the operation
    return prog
