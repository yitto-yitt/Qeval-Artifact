# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np

def create_state_prep():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    # Create a quantum program to prepare the state |01>
    prog = QProg()
    # Apply X gate to first qubit to get |01> state (qiskit's "01" means q1=0, q0=1 in little endian)
    prog << X(qubits[1])
    
    # Execute the program
    machine.directly_run(prog)
    
    return machine, qubits
