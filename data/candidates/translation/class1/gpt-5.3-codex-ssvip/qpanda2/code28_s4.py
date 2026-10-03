# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def visualize_bell_states():
    shots = 1000

    qvm = CPUQVM()
    qvm.init_qvm()

    # phi_plus circuit
    q_phi_plus = qvm.qAlloc_many(2)
    c_phi_plus = qvm.cAlloc_many(2)
    prog_phi_plus = QProg()
    prog_phi_plus << H(q_phi_plus[0]) << CNOT(q_phi_plus[0], q_phi_plus[1])
    prog_phi_plus << Measure(q_phi_plus[0], c_phi_plus[0]) << Measure(q_phi_plus[1], c_phi_plus[1])
    phi_plus_counts = qvm.run_with_configuration(prog_phi_plus, c_phi_plus, shots)

    # phi_minus circuit (as in reference: X on qubit 0, then H, then CNOT)
    q_phi_minus = qvm.qAlloc_many(2)
    c_phi_minus = qvm.cAlloc_many(2)
    prog_phi_minus = QProg()
    prog_phi_minus << X(q_phi_minus[0]) << H(q_phi_minus[0]) << CNOT(q_phi_minus[0], q_phi_minus[1])
    prog_phi_minus << Measure(q_phi_minus[0], c_phi_minus[0]) << Measure(q_phi_minus[1], c_phi_minus[1])
    phi_minus_counts = qvm.run_with_configuration(prog_phi_minus, c_phi_minus, shots)

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    result = {
        "phi_plus": {k: v / phi_plus_total for k, v in phi_plus_counts.items()},
        "phi_minus": {k: v / phi_minus_total for k, v in phi_minus_counts.items()},
    }

    qvm.finalize()
    return result
