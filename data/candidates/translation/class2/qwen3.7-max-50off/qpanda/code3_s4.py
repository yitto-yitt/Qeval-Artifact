# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QuantumMachine, QCircuit, H, CNOT, Measure

def create_ghz(drawing=False):
    qm = QuantumMachine()
    q = qm.qAlloc(3)
    c = qm.cAlloc(3)
    
    cir = QCircuit()
    cir << H(q[0])
    cir << CNOT(q[0], q[1])
    cir << CNOT(q[0], q[2])
    cir << Measure(q[0], c[0])
    cir << Measure(q[1], c[1])
    cir << Measure(q[2], c[2])
    
    if drawing:
        try:
            return cir, cir.draw()
        except Exception:
            return cir, None
    return cir
