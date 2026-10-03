# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    prog = QProg()
    prog << H(0) << CNOT(0, 1)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    probabilities = qvm.get_prob_dict([0, 1])
    return {
        bitstring: float(probability)
        for bitstring, probability in probabilities.items()
        if probability > 0.0
    }
