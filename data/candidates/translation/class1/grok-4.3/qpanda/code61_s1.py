# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, measure

def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = QProg()
    prog << measure(q[0], c[0])
    return prog
