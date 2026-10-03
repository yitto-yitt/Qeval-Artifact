# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init()
    q_plus = qvm.qAlloc_many(2)
    q_minus = qvm.qAlloc_many(2)

    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1])
    result_plus = qvm.probRunDict(prog_plus, q_plus, 1000)

    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1])
    result_minus = qvm.probRunDict(prog_minus, q_minus, 1000)

    total_plus = sum(result_plus.values())
    total_minus = sum(result_minus.values())

    return {
        "phi_plus": {key: value / total_plus for key, value in result_plus.items()},
        "phi_minus": {key: value / total_minus for key, value in result_minus.items()},
    }
