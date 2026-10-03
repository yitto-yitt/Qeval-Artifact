# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init()
    try:
        q = qvm.qAlloc_many(2)
        prog = QProg()
        prog << H(q[0]) << CNOT(q[0], q[1])
        prob_list = qvm.probRunTupleList(prog, q)
        return {state: prob for state, prob in prob_list if prob > 0}
    finally:
        qvm.finalize()
