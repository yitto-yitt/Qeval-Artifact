# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import *

def initialize_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1]) << T(qubits[0])
    return circ
