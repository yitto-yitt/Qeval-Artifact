# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RY, CNOT
import numpy as np

def create_ch_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << RY(qubits[1], np.pi/4)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RY(qubits[1], -np.pi/4)
    return circuit
