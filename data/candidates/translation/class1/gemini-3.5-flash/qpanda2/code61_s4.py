# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc()
    c = machine.cAlloc()
    prog = QProg()
    prog << Measure(q, c)
    return prog
