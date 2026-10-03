# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QuantumMachine, RY, CNOT
import numpy as np

def create_ch_gate():
    machine = QuantumMachine()
    q = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << RY(q[1], np.pi/4) << CNOT(q[0], q[1]) << RY(q[1], -np.pi/4)
    return circuit
