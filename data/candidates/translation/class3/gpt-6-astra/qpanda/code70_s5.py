# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, SWAP, S

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = QProg()
    prog << H(0)
    prog << SWAP(1, 2).control([0])
    prog << H(1)
    prog << S(0).dagger().control([1])
    return prog
