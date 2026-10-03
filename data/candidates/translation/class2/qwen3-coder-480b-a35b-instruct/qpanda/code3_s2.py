# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3 as pq
from pyqpanda3 import *
import numpy as np


def create_ghz(drawing=False):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[0], qubits[2])
    
    # Measure all qubits
    for i in range(3):
        prog << Measure(qubits[i], cbits[i])
    
    if drawing:
        # Since pyQPanda3 doesn't have built-in drawing like Qiskit,
        # we'll return the program and a string representation
        return prog, str(prog)
    else:
        return prog
