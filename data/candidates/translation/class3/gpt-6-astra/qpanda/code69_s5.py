# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, S


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    prog << H(0)
    prog << S(1).control([0])
    prog << H(1)
    prog << S(0).dagger().control([1])
    return prog
