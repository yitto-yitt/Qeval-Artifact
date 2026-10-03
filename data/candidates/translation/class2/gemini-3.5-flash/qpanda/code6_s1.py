# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, X


def create_state_prep(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    prog = QProg()
    if num_qubits > 0:
        prog << X(qubits[0])
    # Attach machine and qubits to the program to prevent garbage collection
    prog.machine = machine
    prog.qubits = qubits
    return prog
