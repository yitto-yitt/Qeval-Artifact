# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *
def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(2)
    cbits = qvm.cAllocMany(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    shots = 1024
    counts = qvm.runWithConfiguration(prog, cbits, shots)
    probabilities_dict = {k: v / shots for k, v in counts.items()}
    return probabilities_dict
