# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    prog = QProg()
    prog.insert(RY(qubits[1], pi/4))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(RY(qubits[1], -pi/4))
    return prog

machine.finalize()
