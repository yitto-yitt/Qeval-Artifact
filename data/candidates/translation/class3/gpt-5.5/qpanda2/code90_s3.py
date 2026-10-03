# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = QCircuit()
    custom << X(qubits[1])
    custom << H(qubits[2])
    custom.set_control([qubits[0], qubits[3]])

    qc2 = QProg()
    qc2 << custom
    return qc2

atexit.register(machine.finalize)
