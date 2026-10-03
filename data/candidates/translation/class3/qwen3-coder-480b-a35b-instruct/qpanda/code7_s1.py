# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(1)
    theta = var("theta")
    prog.insert(RX(qubits[0], theta))
    return prog
