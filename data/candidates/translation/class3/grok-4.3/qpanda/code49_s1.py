# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return circuit
