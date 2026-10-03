# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import QProg, QCircuit, state_vector

def get_statevector(circuit):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
    else:
        prog = circuit
    sv = state_vector(prog)
    return sv
