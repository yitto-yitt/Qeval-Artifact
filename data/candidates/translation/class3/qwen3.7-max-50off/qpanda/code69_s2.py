# EVAL_META: task_id=69, framework=qpanda, class=3
import numpy as np
try:
    from pyqpanda3.core import QuantumCircuit
except ImportError:
    from pyqpanda3 import QuantumCircuit

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    qc.h(0)
    if hasattr(qc, 'cs'):
        qc.cs(0, 1)
    else:
        qc.cp(np.pi/2, 0, 1)
    qc.h(1)
    if hasattr(qc, 'csdg'):
        qc.csdg(1, 0)
    else:
        qc.cp(-np.pi/2, 1, 0)
    return qc
