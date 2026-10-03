# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *


def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])

    result = qvm.prob_run_dict(prog, qubits, -1)
    return {key: float(value) for key, value in result.items() if value != 0}
