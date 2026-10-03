# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, CNOT, X, Measure

def visualize_bell_states():
    qm = QMachine()
    q = qm.qalloc(2)
    c = qm.calloc(2)
    
    prog_plus = QProg()
    prog_plus << H(q[0]) << CNOT(q[0], q[1])
    prog_plus << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    prog_minus = QProg()
    prog_minus << X(q[0]) << H(q[0]) << CNOT(q[0], q[1])
    prog_minus << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    counts_plus = qm.run(prog_plus, 1000)
    counts_minus = qm.run(prog_minus, 1000)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
