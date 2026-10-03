# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, Measure


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    qc = QProg()
    qc << Measure(q[0], c[0])
    return qc
