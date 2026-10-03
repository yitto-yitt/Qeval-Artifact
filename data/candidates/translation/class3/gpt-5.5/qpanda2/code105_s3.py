# EVAL_META: task_id=105, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, CNOT, T

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    circ = QCircuit()
    circ.insert(CNOT(qubits[0], qubits[1]))
    circ.insert(T(qubits[0]))
    return circ


atexit.register(machine.finalize)
