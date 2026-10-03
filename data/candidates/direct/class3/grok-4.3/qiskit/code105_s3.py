# EVAL_META: task_id=105, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral
def initialize_cnot_dihedral():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.t(0)
    return CNOTDihedral(qc)
