# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *

def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[0], q[2])
    circuit << Measure(q[0], c[0])
    circuit << Measure(q[1], c[1])
    circuit << Measure(q[2], c[2])
    
    if drawing:
        prog = QProg()
        prog << circuit
        fig = draw_qprog(prog, 'pic')
        return circuit, fig
    return circuit
