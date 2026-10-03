# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    qc = QuantumCircuit(5)
    
    # Initialize the photon in superposition state on path qubits (qubit 0 and 1)
    qc.h(0)
    qc.x(1)  # This creates |01> + |10> kind of state after the first beam splitter
    
    # First beam splitter - creates superposition
    qc.h(0)
    
    # Bomb interaction - if bomb is present it would interact with the photon
    # Here we simulate the bomb as a CNOT between path qubit and bomb qubit
    qc.cx(0, 2)  # Bomb qubit at index 2, interacts with photon in path 0
    
    # Second beam splitter - interferes the paths
    qc.h(0)
    
    # Additional beam splitter on second path
    qc.h(1)
    
    # Interaction on second path if needed
    qc.cx(1, 3)  # Another possible bomb interaction
    
    # Final interference stage
    qc.h(0)
    qc.h(1)
    
    # Detector setup - these would detect the photon after testing
    qc.cx(0, 4)  # Detector D1
    qc.cx(1, 4)  # Detector D2 - this would detect if bomb was present
    
    return qc
