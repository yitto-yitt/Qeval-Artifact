# EVAL_META: task_id=23, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def dj_constant_oracle():
    oracle = QCircuit()
    oracle << X(qubits[2])

    program = QProg()
    program << oracle
    machine.directly_run(program)

    return oracle
