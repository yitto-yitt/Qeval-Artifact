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
    
    # Convert circuits to CNOTDihedral elements
    elem1 = CNOTDihedral(qc1)
    elem2 = CNOTDihedral(qc2)
    
    # Compose the two elements (elem1 followed by elem2)
    composed = elem1.compose(elem2)
    
    return composed
