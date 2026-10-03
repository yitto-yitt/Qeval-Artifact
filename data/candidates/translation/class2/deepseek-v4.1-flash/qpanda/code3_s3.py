# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, QCircuit, H, CNOT, Measure, draw_qprog

def create_ghz(drawing=False):
    circuit = QCircuit()
    circuit << H(0)
    circuit << CNOT(0, 1)
    circuit << CNOT(0, 2)
    prog = QProg()
    prog << circuit
    prog << Measure(0, 0)
    prog << Measure(1, 1)
    prog << Measure(2, 2)
    if drawing:
        return prog, draw_qprog(prog, 'pic')
    return prog
