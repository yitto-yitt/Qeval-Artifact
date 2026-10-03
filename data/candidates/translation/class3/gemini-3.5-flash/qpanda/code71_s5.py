# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import *

class MachineContainer:
    machine = None

def create_quantum_circuit_based_h0_csx01_h1():
    if MachineContainer.machine is None:
        MachineContainer.machine = CPUQVM()
        MachineContainer.machine.init_qvm()
    else:
        MachineContainer.machine.init_qvm()
        
    machine = MachineContainer.machine
    q = machine.qAlloc_many(3)
    prog = QProg()
    prog << H(q[0])
    prog << SX(q[1]).control([q[0]])
    prog << H(q[1])
    return prog
