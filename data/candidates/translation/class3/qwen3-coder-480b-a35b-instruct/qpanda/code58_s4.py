# EVAL_META: task_id=58, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def create_ch_gate():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << RY(qubits[1], math.pi/4) << CNOT(qubits[0], qubits[1]) << RY(qubits[1], -math.pi/4)
    
    pq.destroy_quantum_machine(machine)
    return prog
