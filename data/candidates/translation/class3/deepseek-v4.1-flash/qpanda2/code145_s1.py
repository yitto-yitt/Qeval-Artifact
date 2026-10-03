# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def qft_inverse(n):
    return QFT_inverse(qubits[:n])

if __name__ == "__main__":
    machine.finalize()
