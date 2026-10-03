# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, RY, X

def tensor_circuits():
    tensored = QProg()
    tensored << X(0)
    tensored << RY(2, 0.2).control([1])
    simulator = CPUQVM()
    simulator.run(tensored, 1)
    return tensored
