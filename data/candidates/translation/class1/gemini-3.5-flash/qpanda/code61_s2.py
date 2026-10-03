# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import *


def create_quantum_circuit_with_one_qubit_and_measure():
    try:
        init_quantum_machine(QMachineType.CPU)
    except Exception:
        pass
    q = qAlloc()
    c = cAlloc()
    prog = QProg()
    prog << Measure(q, c)
    return prog
