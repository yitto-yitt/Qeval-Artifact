# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *

def create_ghz(drawing=False):
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAllocList(3)
    c = qvm.cAllocList(3)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])
    
    if drawing:
        try:
            fig = draw_qprog(prog, output='mpl')
            return prog, fig
        except Exception:
            return prog, None
    return prog
