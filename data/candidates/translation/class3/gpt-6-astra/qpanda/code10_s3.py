# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, X


def create_operator():
    program = QProg()
    program << X(0) << X(1)
    simulator = CPUQVM()
    simulator.run(program, 1)
    return program
