# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    circuit = QCircuit()
    circuit << CRY(qubits[0], qubits[1], 0.2)
    circuit << X(qubits[2])
    return circuit

machine.finalize()
