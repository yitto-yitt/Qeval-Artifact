# EVAL_META: task_id=130, framework=qiskit, class=3
from qiskit import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    qc.h(1)
    qc.h(2)
    qc.cx(1, 3)
    qc.cx(2, 4)
    return qc.inverse()
