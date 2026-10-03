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
    qc.cx(0, 2)  # If photon goes through path where bomb is, entangle with bomb qubit
    
    # Second beam splitter
    qc.h(0)
    
    # Interference setup - second path qubit
    qc.cx(0, 1)  # Entangle paths
    qc.h(1)
    
    # Add additional ancilla qubits to represent possible bomb states
    qc.h(3)
    qc.cx(3, 4)
    
    # Final interference
    qc.cx(1, 4)
    qc.h(4)
    
    return qc
