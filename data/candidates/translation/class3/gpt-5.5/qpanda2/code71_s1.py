# EVAL_META: task_id=71, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(qubits[0])
    prog << U1(qubits[0], math.pi / 4)
    prog << RX(qubits[1], math.pi / 2).control([qubits[0]])
    prog << H(qubits[1])
    return prog
