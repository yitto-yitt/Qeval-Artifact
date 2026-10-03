# EVAL_META: task_id=60, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    prog = QProg()
    prog << S_dagger(qubits[1])
    prog << CNOT(qubits[0], qubits[1])
    prog << S(qubits[1])
    machine.directly_run(prog)
    return prog

machine.finalize()
