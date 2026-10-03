# EVAL_META: task_id=12, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def get_unitary():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return Operator(qc).data
