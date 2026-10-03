# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(2)
    prog = QProg()
    prog << H(qubits[0]) << CRZ(qubits[0], qubits[1], theta) << H(qubits[1]) << CRY(qubits[1], qubits[0], theta)
    return prog
