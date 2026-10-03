# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *

def visualize_bell_states():
    init(QMachineType.CPU)
    shots = 1000
    try:
        qp = qAlloc_many(2)
        cp = cAlloc_many(2)
        prog_p = QProg()
        prog_p << H(qp[0]) << CNOT(qp[0], qp[1]) << MeasureAll(qp, cp)
        counts_p = run_with_configuration(prog_p, cp, shots)

        qm = qAlloc_many(2)
        cm = cAlloc_many(2)
        prog_m = QProg()
        prog_m << X(qm[0]) << H(qm[0]) << CNOT(qm[0], qm[1]) << MeasureAll(qm, cm)
        counts_m = run_with_configuration(prog_m, cm, shots)
    finally:
        finalize()

    return {
        "phi_plus": {key: value / shots for key, value in counts_p.items()},
        "phi_minus": {key: value / shots for key, value in counts_m.items()},
    }
