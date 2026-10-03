# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CS, CSdg

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    q = prog.alloc(2)
    prog << H(q[0])
    prog << CS(q[0], q[1])
    prog << H(q[1])
    prog << CSdg(q[1], q[0])
    return prog
