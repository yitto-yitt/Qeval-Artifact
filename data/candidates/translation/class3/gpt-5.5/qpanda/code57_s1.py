# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, CNOT

def create_swap_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[1], q[0])
    circuit << CNOT(q[0], q[1])
    return circuit
