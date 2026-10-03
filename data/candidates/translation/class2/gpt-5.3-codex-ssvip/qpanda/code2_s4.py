# EVAL_META: task_id=2, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *

def create_bell_statevector():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    simulator = StatevectorSimulator()
    state = simulator.simulate(prog, q)
    machine.finalize()
    return state
