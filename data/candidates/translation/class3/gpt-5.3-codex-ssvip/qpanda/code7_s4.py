# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RX


def create_parametrized_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc()
    theta = 0.0
    circuit = QCircuit()
    circuit << RX(q, theta)
    return circuit
