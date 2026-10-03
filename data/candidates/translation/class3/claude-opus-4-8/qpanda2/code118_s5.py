# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = QProg()
    prog << X(qubits[3]).control([qubits[0], qubits[1], qubits[2]])
    prog << RZ(qubits[3], -PI / 4).control([qubits[0], qubits[1], qubits[2]])
    prog << X(qubits[3]).control([qubits[0], qubits[1], qubits[2]])
    prog << RZ(qubits[3], PI / 4).control([qubits[0], qubits[1], qubits[2]])
    return prog

machine.finalize()
