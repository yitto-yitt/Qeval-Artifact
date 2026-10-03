# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    qvm.set_state(desired_vector)
    prog = QProg()
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1]) << Measure(qubits[2], cbits[2])
    result = qvm.run_with_configuration(prog, shots=1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
