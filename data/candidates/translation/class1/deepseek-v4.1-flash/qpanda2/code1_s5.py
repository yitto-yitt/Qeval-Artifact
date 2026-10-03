# EVAL_META: task_id=1, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure


def run_bell_state_simulator():
    machine = CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
