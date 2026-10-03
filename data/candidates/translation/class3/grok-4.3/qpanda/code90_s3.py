# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QProg, X, H

def create_custom_controlled():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(4)
    qc1 = QCircuit()
    qc1 << X(qubits[1]) << H(qubits[2])
    custom = qc1.control([qubits[0], qubits[3]])
    qc2 = QProg()
    qc2 << custom
    return qc2
