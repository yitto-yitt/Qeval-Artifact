# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def create_quantum_circuit_based_h0_csx01_h1():
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(3)
    prog = QProg()
    prog << H(qubits[0]) << CRX(qubits[0], qubits[1], pi/2) << H(qubits[1])
    return prog
