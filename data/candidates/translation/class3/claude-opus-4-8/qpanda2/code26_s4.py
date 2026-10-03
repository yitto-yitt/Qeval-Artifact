# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


def bell_dag():
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0])
    dag = prog_to_dag(prog)
    return dag


machine.finalize()
