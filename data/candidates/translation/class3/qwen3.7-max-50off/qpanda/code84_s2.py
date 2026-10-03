# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, CU3

def controlled_custom_unitary_circuit():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = qm.create_empty_qprog()
    prog << CU3(q[0], q[1], 0.3, 0.2, 0.1)
    return prog
