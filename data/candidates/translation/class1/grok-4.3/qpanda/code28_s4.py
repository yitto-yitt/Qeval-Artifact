# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, Measure

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    result_plus = qvm.run_with_configuration(prog_plus, c, shots=1000)
    total_plus = sum(result_plus.values())
    prob_plus = {k: v / total_plus for k, v in result_plus.items()}

    qvm2 = CPUQVM()
    qvm2.init_qvm()
    q2 = qvm2.qAlloc_many(2)
    c2 = qvm2.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])
    result_minus = qvm2.run_with_configuration(prog_minus, c2, shots=1000)
    total_minus = sum(result_minus.values())
    prob_minus = {k: v / total_minus for k, v in result_minus.items()}

    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus,
    }
