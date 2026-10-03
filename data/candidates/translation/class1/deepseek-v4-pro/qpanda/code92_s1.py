# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, H, CNOT, Stabilizer

def calculate_stabilizer_state_info():
    q = Qubit(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    stab = Stabilizer()
    stab.init(prog)
    probs = stab.probabilities_dict()
    return probs
