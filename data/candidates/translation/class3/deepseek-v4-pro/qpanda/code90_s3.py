# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(4)

    custom = QCircuit()
    custom << X(q[1]) << H(q[2])
    controlled_custom = custom.control([q[0], q[3]])

    final_circuit = QCircuit()
    final_circuit << controlled_custom
    return final_circuit
