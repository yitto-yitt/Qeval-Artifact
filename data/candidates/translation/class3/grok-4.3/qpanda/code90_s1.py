# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, X, H

def create_custom_controlled():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(4)
    circuit = QCircuit()
    circuit << X(q[1]).control([q[0], q[3]])
    circuit << H(q[2]).control([q[0], q[3]])
    return circuit
