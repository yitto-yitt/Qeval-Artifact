# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, RZ, RY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QProg()
    prog << H(0)
    prog << RZ(1, theta).control([0])
    prog << H(1)
    prog << RY(0, theta).control([1])
    simulator = CPUQVM()
    simulator.run(prog, 1)
    return prog
