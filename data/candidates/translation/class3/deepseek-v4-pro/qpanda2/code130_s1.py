# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()

def inv_circuit(n):
    qubits = qvm.qAlloc_many(n)

    qc = QCircuit()
    qc << H(qubits[1])
    qc << H(qubits[2])
    qc << CNOT(qubits[1], qubits[3])
    qc << CNOT(qubits[2], qubits[4])

    return qc.dagger()

qvm.finalize()
