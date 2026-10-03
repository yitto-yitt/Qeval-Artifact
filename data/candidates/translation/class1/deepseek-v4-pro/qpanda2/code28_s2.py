# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    shots = 1000

    init_qvm()
    qvm = QVM()

    q_pp = qvm.qAlloc_many(2)
    c_pp = qvm.cAlloc_many(2)
    prog_pp = QProg()
    prog_pp << H(q_pp[0]) << CNOT(q_pp[0], q_pp[1]) << measure(q_pp[0], c_pp[0]) << measure(q_pp[1], c_pp[1])
    counts_pp = qvm.run_with_configuration(prog_pp, c_pp, shots)

    q_pm = qvm.qAlloc_many(2)
    c_pm = qvm.cAlloc_many(2)
    prog_pm = QProg()
    prog_pm << X(q_pm[0]) << H(q_pm[0]) << CNOT(q_pm[0], q_pm[1]) << measure(q_pm[0], c_pm[0]) << measure(q_pm[1], c_pm[1])
    counts_pm = qvm.run_with_configuration(prog_pm, c_pm, shots)

    pp_total = builtins.sum(counts_pp.values())
    pm_total = builtins.sum(counts_pm.values())

    return {
        "phi_plus": {bit: count / pp_total for bit, count in counts_pp.items()},
        "phi_minus": {bit: count / pm_total for bit, count in counts_pm.items()},
    }
