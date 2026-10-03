# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(0, 1, theta)
    qc.h(1)
    qc.cry(1, 0, theta)
    return qc
