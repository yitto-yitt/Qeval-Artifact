# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    top = QCircuit()
    top << X(qubits[2])
    bottom = QCircuit()
    bottom << RY(qubits[1], 0.2).control(qubits[0])
    return bottom.tensor(top)

machine.finalize()
