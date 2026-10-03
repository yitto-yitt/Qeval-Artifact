# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QProg, qalloc, H, SWAP, SDG, Control

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    q = qalloc(3)
    prog = QProg()
    prog << H(q[0])
    prog << Control(q[0], SWAP(q[1], q[2]))
    prog << H(q[1])
    prog << Control(q[1], SDG(q[0]))
    return prog
