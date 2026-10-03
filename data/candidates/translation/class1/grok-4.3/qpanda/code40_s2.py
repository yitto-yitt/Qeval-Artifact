# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, initialize, Measure

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog << initialize(desired_vector, qubits)
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    prog << Measure(qubits[2], cbits[2])
    counts = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    bit_counts = {}
    for k, v in counts.items():
        bitstr = bin(k)[2:].zfill(3)
        bit_counts[bitstr] = bit_counts.get(bitstr, 0) + v
    return {key: value / total for key, value in bit_counts.items()}
