# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    qc = QuantumCircuit(5)
    
    # Initialize the photon in superposition on path A and B
    qc.h(0)  # Photon starts in superposition of path 0 and path 1
    
    # First beam splitter creates superposition
    qc.h(1)  # Ancilla qubit representing bomb presence
    
    # Interaction between photon and bomb (if present)
    qc.cx(0, 1)  # CNOT gate represents interaction
    
    # Second beam splitter to recombine paths
    qc.h(0)
    
    # Additional ancilla qubits to represent the setup more completely
    qc.h(2)  # Another possible path
    qc.cx(0, 2)
    qc.h(2)
    
    # Add some additional control to simulate the interferometer setup
    qc.h(3)
    qc.cx(1, 3)
    qc.h(3)
    
    qc.h(4)
    qc.cx(2, 4)
    qc.h(4)
    
    return qc
