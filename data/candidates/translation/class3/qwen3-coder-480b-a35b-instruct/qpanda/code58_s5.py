# EVAL_META: task_id=58, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def create_ch_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(RY(qubits[1], math.pi/4))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(RY(qubits[1], -math.pi/4))
    
    return prog, qubits, machine
