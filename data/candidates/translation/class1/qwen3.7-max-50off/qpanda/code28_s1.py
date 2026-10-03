# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, X, CNOT, Measure

def visualize_bell_states():
    shots = 1000
    
    qm_plus = QMachine()
    q_plus = qm_plus.qAlloc(2)
    c_plus = qm_plus.cAlloc(2)
    prog_plus = QProg()
    prog_plus << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1])
    prog_plus << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
    counts_plus = qm_plus.run(prog_plus, shots)
    
    qm_minus = QMachine()
    q_minus = qm_minus.qAlloc(2)
    c_minus = qm_minus.cAlloc(2)
    prog_minus = QProg()
    prog_minus << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1])
    prog_minus << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
    counts_minus = qm_minus.run(prog_minus, shots)
    
    def to_probs(counts):
        total = sum(counts.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in counts.items()}
        
    return {
        "phi_plus": to_probs(counts_plus),
        "phi_minus": to_probs(counts_minus)
    }
