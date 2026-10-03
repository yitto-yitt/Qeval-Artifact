# EVAL_META: task_id=58, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QCircuit, RY, CNOT

_global_qvm_holder = []

def create_ch_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    _global_qvm_holder.append(qvm)
    q = qvm.qAlloc_many(2)
    
    circuit = QCircuit()
    circuit << RY(q[1], np.pi/4) << CNOT(q[0], q[1]) << RY(q[1], -np.pi/4)
    return circuit
