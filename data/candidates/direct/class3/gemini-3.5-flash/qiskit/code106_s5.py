# EVAL_META: task_id=106, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral

def compose_cnot_dihedral():
    # Create the first quantum circuit
    qc1 = QuantumCircuit(2)
    qc1.cx(0, 1)
    qc1.t(0)
    
    # Create the second quantum circuit
    qc2 = QuantumCircuit(2)
    qc2.cx(0, 1)
    qc2.t(0)
    qc2.x(1)
    
    # Convert to CNOTDihedral elements
    cd1 = CNOTDihedral(qc1)
    cd2 = CNOTDihedral(qc2)
    
    # Compose the CNOTDihedral elements (cd1 followed by cd2)
    composed_cd = cd1.compose(cd2)
    
    return composed_cd
