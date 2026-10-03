# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import CPUQVM, qAlloc_many, QCircuit, X, CRY

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(3)

def tensor_circuits():
    circ = QCircuit()
    circ << X(qubits[0])
    circ << CRY(qubits[1], qubits[2], 0.2)
    return circ

machine.finalize()
