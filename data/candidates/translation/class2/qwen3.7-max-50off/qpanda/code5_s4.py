# EVAL_META: task_id=5, framework=qpanda, class=2
import pyqpanda3

def create_state_prep():
    qm = pyqpanda3.QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = pyqpanda3.QProg()
    prog << pyqpanda3.X(q[0])
    return prog
