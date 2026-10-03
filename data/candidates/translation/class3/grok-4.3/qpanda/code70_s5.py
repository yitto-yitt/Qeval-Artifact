# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, H, CSWAP, CSDG

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qm = QuantumMachine()
    q = qm.qAlloc_many(3)
    cir = QCircuit()
    cir << H(q[0])
    cir << CSWAP(q[0], q[1], q[2])
    cir << H(q[1])
    cir << CSDG(q[1], q[0])
    return cir
