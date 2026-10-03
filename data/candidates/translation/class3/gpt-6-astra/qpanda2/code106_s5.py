# EVAL_META: task_id=106, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, CNOT, T, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(qubits[0], qubits[1]) << T(qubits[0])

    circ2 = QCircuit()
    circ2 << CNOT(qubits[0], qubits[1]) << T(qubits[0]) << X(qubits[1])

    composed = QCircuit()
    composed << circ1 << circ2

    program = QProg()
    program << composed
    machine.directly_run(program)
    return composed


atexit.register(machine.finalize)
