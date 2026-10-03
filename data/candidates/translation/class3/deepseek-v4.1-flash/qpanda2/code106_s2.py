# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    circuit = QCircuit()
    circuit << T(qubits[0]) << T(qubits[0]) << X(qubits[1])
    return circuit

machine.finalize()
