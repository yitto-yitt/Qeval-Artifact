# EVAL_META: task_id=130, framework=qiskit, class=3
from qiskit import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    qc.h(1)
    qc.h(2)
    qc.cx(1, 3)
    qc.cx(2, 4)
    if hasattr(qc, 'inverse'):
        return qc.inverse()
    else:
        inv_qc = QuantumCircuit(n)
        inv_qc.cx(2, 4)
        inv_qc.cx(1, 3)
        inv_qc.h(2)
        inv_qc.h(1)
        return inv_qc
