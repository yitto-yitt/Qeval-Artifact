# EVAL_META: task_id=130, framework=qiskit, class=3
from qiskit import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    if n > 1:
        qc.h(1)
    if n > 2:
        qc.h(2)
    if n > 3:
        qc.cx(1, 3)
    if n > 4:
        qc.cx(2, 4)
    return qc.inverse()
