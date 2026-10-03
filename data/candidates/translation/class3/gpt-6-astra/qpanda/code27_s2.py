# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3 import core


def apply_op_back():
    program = core.QProg()
    program << core.H(0)
    program << core.CNOT(0, 1)
    program << core.H(0)

    simulator = core.CPUQVM()
    simulator.run(program, 1)

    dag_type = getattr(core, "QProgDAG", None)
    if dag_type is not None:
        return dag_type(program)
    return program
