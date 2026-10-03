# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    circuit = QCircuit()
    circuit << QGate("H", qubits[2]).control([qubits[0], qubits[1]])
    return circuit

machine.finalize()
