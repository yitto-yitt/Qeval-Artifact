# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, CNOTDihedral, CPUQVM

def initialize_cnot_dihedral():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    elem = CNOTDihedral(circ)
    return elem
