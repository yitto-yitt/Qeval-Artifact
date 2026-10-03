# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def calculate_stabilizer_state_info():
    circuit = QCircuit()
    circuit << H(0)
    circuit << CNOT(0, 1)

    prog = QProg()
    prog << circuit

    qvm = CPUQVM()
    qvm.run(prog, 100000)
    result = qvm.result()
    counts = result.get_counts()

    total = sum(counts.values())
    probabilities_dict = {}
    for state, count in counts.items():
        key = state.zfill(2)
        probabilities_dict[key] = count / total

    return probabilities_dict
