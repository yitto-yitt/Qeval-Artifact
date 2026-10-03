# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    prog = QProg()
    prog << H(0) << CNOT(0, 1)

    qvm = CPUQVM()
    qvm.run(prog)
    probabilities = qvm.result().get_prob_dict()
    return {bits: float(prob) for bits, prob in probabilities.items() if prob > 0.0}
