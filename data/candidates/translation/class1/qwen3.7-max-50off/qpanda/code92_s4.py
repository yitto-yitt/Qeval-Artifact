# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qm = QMachine(2)
    q = qm.qubits
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prob_dict = qm.get_prob_dict(q, prog)
    return prob_dict
