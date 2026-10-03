# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, CSX

def create_quantum_circuit_based_h0_csx01_h1():
    qc = QuantumCircuit(3)
    qc << H(qc[0])
    qc << CSX(qc[0], qc[1])
    qc << H(qc[1])
    return qc
