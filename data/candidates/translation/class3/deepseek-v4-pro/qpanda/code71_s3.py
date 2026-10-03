# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CSX

def create_quantum_circuit_based_h0_csx01_h1():
    qc = QCircuit(3)
    qc << H(0) << CSX(0, 1) << H(1)
    return qc
