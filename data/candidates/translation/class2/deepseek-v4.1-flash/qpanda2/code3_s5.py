# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *

def create_ghz(drawing=False):
    qubits = [Qubit(i) for i in range(3)]
    cbits = [CBit(i) for i in range(3)]
    
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[0], qubits[2])
    prog << measure(qubits[0], cbits[0])
    prog << measure(qubits[1], cbits[1])
    prog << measure(qubits[2], cbits[2])
    
    if drawing:
        try:
            fig = draw_qprog(prog, 'pic')
        except:
            fig = str(prog)
        return prog, fig
    return prog
