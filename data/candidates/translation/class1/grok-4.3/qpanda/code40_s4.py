# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, state_preparation, measure
def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = QProg()
    prog << state_preparation(q, desired_vector)
    prog << measure(q, c)
    machine.set_random_seed(42)
    result = machine.run_with_configuration(prog, c, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
