# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *
import math
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << U1(q[0], math.pi / 4)
    circuit << RX(q[1], math.pi / 2).control([q[0]])
    circuit << H(q[1])
    return circuit

atexit.register(machine.finalize)
