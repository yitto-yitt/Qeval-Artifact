# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QProg, H, CNOT

def inv_circuit(n):
    qvm = QMachine()
    q = qvm.qAlloc(n)
    prog = QProg()
    prog << H(q[1]) << H(q[2])
    prog << CNOT(q[1], q[3]) << CNOT(q[2], q[4])
    return prog.dagger()
