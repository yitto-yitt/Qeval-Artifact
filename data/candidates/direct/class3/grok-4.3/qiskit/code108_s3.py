# EVAL_META: task_id=108, framework=qiskit, class=3
from qiskit.quantum_info import Choi
def initialize_adjoint_and_compose(data1, data2):
    c1 = Choi(data1)
    c2 = Choi(data2)
    adj = c1.adjoint()
    comp = c1.compose(c2)
    return c1, adj, comp
