# EVAL_META: task_id=106, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral

def compose_cnot_dihedral():
    # Create first quantum circuit
    qc1 = QuantumCircuit(2)
    qc1.cx(0, 1)
    qc1.t(0)
    
    # Create second quantum circuit
    qc2 = QuantumCircuit(2)
    qc2.cx(0, 1)
    qc2.t(0)
    qc2.x(1)
    
    # Convert to CNOTDihedral elements
    cnot_dihedral1 = CNOTDihedral(qc1)
    cnot_dihedral2 = CNOTDihedral(qc2)
    
    # Compose the circuits
    composed = cnot_dihedral1.compose(cnot_dihedral2)
    
    return composed
