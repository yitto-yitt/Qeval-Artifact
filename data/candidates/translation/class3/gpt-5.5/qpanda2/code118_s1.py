# EVAL_META: task_id=118, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
atexit.register(machine.finalize)

def create_c3sx_circuit():
    prog = QProg()
    prog << U1(qubits[2], math.pi / 4).control([qubits[0], qubits[1]])
    prog << RX(qubits[3], math.pi / 2).control([qubits[0], qubits[1], qubits[2]])
    return prog
