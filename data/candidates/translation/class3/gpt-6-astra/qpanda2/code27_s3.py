# EVAL_META: task_id=27, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QProg, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


def apply_op_back():
    program = QProg()
    program << H(qubits[0])
    program << CNOT(qubits[0], qubits[1])
    program << H(qubits[0])
    machine.directly_run(program)
    return program


atexit.register(machine.finalize)
