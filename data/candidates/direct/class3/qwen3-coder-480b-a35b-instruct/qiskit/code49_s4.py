# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    qc = QuantumCircuit(5)
    
    # Initialize the photon in superposition state on path qubits (qubit 0 and 1)
    qc.h(0)  # Create superposition on first path qubit
    
    # First beam splitter creates superposition between paths
    qc.cx(0, 1)  # Entangle path qubits
    qc.h(0)
    
    # Bomb interaction - if bomb is present it blocks one path
    # Here we simulate the bomb by adding an interaction on one path
    qc.cx(1, 2)  # Interaction with bomb qubit (qubit 2), if bomb is live
    
    # Second beam splitter to recombine paths
    qc.h(0)
    qc.cx(0, 1)
    
    # Additional interferometer components
    qc.h(3)  # Ancilla qubit for detection
    qc.cx(1, 3)  # Entangle path with detector
    
    # Add another ancilla to represent possible bomb detonation
    qc.cx(2, 4)  # If bomb was triggered, affect output
    
    return qc
