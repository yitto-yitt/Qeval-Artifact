# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def bell_each_shot():
    shots = 10
    qvm = init_quantum_machine(QMachineType.CPU)
    try:
        q = qvm.qAlloc_many(2)
        c = qvm.cAlloc_many(2)

        prog = QProg()
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        prog << Measure(q[0], c[0])
        prog << Measure(q[1], c[1])

        counts = qvm.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        destroy_quantum_machine(qvm)
