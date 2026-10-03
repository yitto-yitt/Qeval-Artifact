# EVAL_META: task_id=44, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    top = QCircuit()
    top.insert(X(qubits[2]))

    bottom = QCircuit()
    bottom.insert(RY(qubits[1], 0.2).control([qubits[0]]))

    tensored = QCircuit()
    tensored.insert(bottom)
    tensored.insert(top)
    return tensored

atexit.register(machine.finalize)
