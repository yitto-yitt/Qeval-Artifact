# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    program = QProg()
    program << H(0) << CNOT(0, 1)

    simulator = CPUQVM()
    simulator.run(program, 1)
    return simulator.result().get_state_vector()
