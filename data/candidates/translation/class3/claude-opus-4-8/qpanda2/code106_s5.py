# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, CNOT, T, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    circ << X(qubits[1])
    return circ


composed = compose_cnot_dihedral()
machine.finalize()
