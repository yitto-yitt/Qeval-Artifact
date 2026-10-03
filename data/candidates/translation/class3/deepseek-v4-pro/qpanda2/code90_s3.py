# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(4)

def create_custom_controlled():
    custom = QCircuit()
    custom << X(qubits[1]) << H(qubits[2])
    return custom.control([qubits[0], qubits[3]])

qvm.finalize()
