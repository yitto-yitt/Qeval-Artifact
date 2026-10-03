# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM, PGate, RX

def create_parametrized_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)

    theta = PGate("theta")
    circuit = QCircuit()
    circuit << RX(q[0], theta)

    prog = QProg()
    prog << circuit

    return circuit
