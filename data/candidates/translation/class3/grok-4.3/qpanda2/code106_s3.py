# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(qubits[0], qubits[1]) << T(qubits[0])
    circ2 = QCircuit()
    circ2 << CNOT(qubits[0], qubits[1]) << T(qubits[0]) << X(qubits[1])
    composed_circ = QCircuit()
    composed_circ << circ2 << circ1
    return composed_circ
machine.finalize()
