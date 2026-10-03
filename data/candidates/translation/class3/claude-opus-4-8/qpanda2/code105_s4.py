# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, CNOT, T

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    return circ


if __name__ == "__main__":
    elem = initialize_cnot_dihedral()
    print(elem)
    machine.finalize()
