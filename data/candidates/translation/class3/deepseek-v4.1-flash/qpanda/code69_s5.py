# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CS, CSDG, qAlloc_many

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    q = qAlloc_many(2)
    qc = QCircuit()
    qc << H(q[0])
    qc << CS(q[0], q[1])
    qc << H(q[1])
    qc << CSDG(q[1], q[0])
    return qc
