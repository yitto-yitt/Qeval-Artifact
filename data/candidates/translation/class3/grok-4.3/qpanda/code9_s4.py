# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_efficientSU2():
    qc = QuantumCircuit(3)
    for i in range(3):
        qc.ry(f"θ_{i}", i)
        qc.rz(f"φ_{i}", i)
    qc.barrier()
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.barrier()
    for i in range(3):
        qc.ry(f"θ_{i+3}", i)
        qc.rz(f"φ_{i+3}", i)
    return qc
