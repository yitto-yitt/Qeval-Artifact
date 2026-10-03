# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RX
import math

def create_c3sx_circuit():
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(4)
    circuit = QCircuit()
    sx = RX(qubits[3], math.pi / 2)
    circuit << sx.control(qubits[0]).control(qubits[1]).control(qubits[2])
    return circuit
