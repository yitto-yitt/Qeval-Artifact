# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import CPUQVM, qAlloc_many, QCircuit, H, CNOT, convert_qprog_to_originir

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(3)


def bell_dag():
    circ = QCircuit()
    circ.insert(H(qubits[0]))
    circ.insert(CNOT(qubits[0], qubits[1]))
    return circ


machine.finalize()
