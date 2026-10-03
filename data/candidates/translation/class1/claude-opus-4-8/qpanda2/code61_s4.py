# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import CPUQVM, measure_all


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = measure_all(q, c)
    return prog
