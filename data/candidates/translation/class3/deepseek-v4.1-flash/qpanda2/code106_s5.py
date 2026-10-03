# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    composed = QCircuit()
    composed << CNOT(qubits[0], qubits[1])
    composed << T(qubits[0])
    composed << CNOT(qubits[0], qubits[1])
    composed << T(qubits[0])
    composed << X(qubits[1])
    return composed

machine.finalize()
