# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import *

def visualize_bell_states():
    def run_bell(phi_minus=False):
        qvm = CPUQVM()
        qvm.init_qvm()
        q = qvm.qAlloc_many(2)
        c = qvm.cAlloc_many(2)
        prog = QProg()
        if phi_minus:
            prog << X(q[0])
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        prog << Measure(q[0], c[0])
        prog << Measure(q[1], c[1])
        counts = qvm.run_with_configuration(prog, c, 1000)
        qvm.finalize()
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    
    return {
        "phi_plus": run_bell(phi_minus=False),
        "phi_minus": run_bell(phi_minus=True)
    }
