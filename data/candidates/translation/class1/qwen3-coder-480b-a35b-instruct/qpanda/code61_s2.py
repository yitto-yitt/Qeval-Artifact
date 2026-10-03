# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import *

def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = QProg()
    prog << measure_all(q, c)
    return prog
