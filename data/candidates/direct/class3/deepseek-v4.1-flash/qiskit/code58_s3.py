# EVAL_META: task_id=58, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit

def create_ch_gate():
    qc = QuantumCircuit(2, name="ch")
    qc.ry(-math.pi / 4, 1)
    qc.cx(0, 1)
    qc.ry(math.pi / 4, 1)
    return qc
