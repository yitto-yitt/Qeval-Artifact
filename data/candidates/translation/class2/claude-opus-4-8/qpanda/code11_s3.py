# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import QProg, state_vector

def get_statevector(circuit):
    prog = QProg()
    prog << circuit
    sv = state_vector(prog)
    return sv
