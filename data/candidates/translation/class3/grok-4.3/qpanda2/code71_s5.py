# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(qubits[0])
    sx = U3(qubits[1], math.pi/2, -math.pi/2, math.pi/2)
    prog << sx.control([qubits[0]])
    prog << H(qubits[1])
    return prog

machine.finalize()
