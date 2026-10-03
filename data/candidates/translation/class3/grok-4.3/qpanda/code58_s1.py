# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RY, CNOT
from numpy import pi

def create_ch_gate():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAllocMany(2)
    circuit = QCircuit()
    circuit << RY(q[1], pi/4) << CNOT(q[0], q[1]) << RY(q[1], -pi/4)
    return circuit
