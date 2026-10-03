# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    result_plus = qvm.run_with_configuration(prog_plus, c, 1000)
    prog_minus = QProg()
    prog_minus << X(q[0]) << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    result_minus = qvm.run_with_configuration(prog_minus, c, 1000)
    shots = 1000
    phi_plus_dist = {k: v / shots for k, v in result_plus.items()}
    phi_minus_dist = {k: v / shots for k, v in result_minus.items()}
    return {"phi_plus": phi_plus_dist, "phi_minus": phi_minus_dist}
