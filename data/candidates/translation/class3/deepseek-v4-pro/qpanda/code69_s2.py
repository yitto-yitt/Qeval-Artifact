# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cs(0, 1)
    qc.h(1)
    qc.csdg(1, 0)
    return qc
