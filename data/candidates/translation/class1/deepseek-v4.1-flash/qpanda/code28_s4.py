# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure

def visualize_bell_states():
    machine = CPUQVM()
    machine.init_qvm()
    
    # phi_plus
    q_plus = machine.qAlloc_many(2)
    c_plus = machine.cAlloc_many(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1])
    prog_plus << measure(q_plus[0], c_plus[0])
    prog_plus << measure(q_plus[1], c_plus[1])
    counts_plus = machine.run_with_configuration(prog_plus, c_plus, 1000)
    
    # phi_minus
    q_minus = machine.qAlloc_many(2)
    c_minus = machine.cAlloc_many(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1])
    prog_minus << measure(q_minus[0], c_minus[0])
    prog_minus << measure(q_minus[1], c_minus[1])
    counts_minus = machine.run_with_configuration(prog_minus, c_minus, 1000)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()},
    }
