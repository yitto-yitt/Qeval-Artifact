# EVAL_META: task_id=66, framework=qpanda2, class=2
import math
from pyqpanda import *

def w_state():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    prog = QProg()
    
    # RY gate with angle 2*arccos(1/sqrt(3))
    theta = 2 * math.acos(1 / math.sqrt(3))
    prog << RY(qubits[0], theta)
    
    # CH gate (Controlled-Hadamard)
    prog << CNOT(qubits[0], qubits[1])  # This creates the controlled operation structure
    
    # CX gates
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    
    # X gate on qubit 0
    prog << X(qubits[0])
    
    # Measure all qubits
    cregs = machine.cAlloc_many(3)
    for i in range(3):
        prog << Measure(qubits[i], cregs[i])
    
    return prog
