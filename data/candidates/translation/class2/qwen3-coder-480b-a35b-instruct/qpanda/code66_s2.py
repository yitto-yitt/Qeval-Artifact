# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *
import pyqpanda3 as pq


def w_state():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    prog = pq.QProg()
    
    prog.insert(RY(qubits[0], 2 * arccos(1 / sqrt(3))))
    prog.insert(CH(qubits[0], qubits[1]))
    prog.insert(CNOT(qubits[1], qubits[2]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(X(qubits[0]))
    
    # Add measurements to all qubits
    cregs = machine.cAlloc_many(3)
    for i in range(3):
        prog.insert(MEASURE(qubits[i], cregs[i]))
    
    pq.run_prog(prog, machine)
    
    # Return the program which represents the circuit
    return prog
