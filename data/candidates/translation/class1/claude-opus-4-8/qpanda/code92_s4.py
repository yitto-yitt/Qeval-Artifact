# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT

def calculate_stabilizer_state_info():
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)

    prog = QProg()
    prog << qc

    qvm = CPUQVM()
    qvm.run(prog, 0)
    result = qvm.result()
    probs = result.get_prob_dict()

    probabilities_dict = {k: v for k, v in probs.items() if v > 1e-12}
    return probabilities_dict
