# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import QProg

def get_statevector(circuit):
    prog = QProg()
    prog << circuit
    from pyqpanda3.core import state_vector
    sv = state_vector(prog)
    return sv
