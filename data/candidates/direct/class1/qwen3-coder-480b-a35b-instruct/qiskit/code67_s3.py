# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    """
    Creates a CHSH (Clauser-Horne-Shimony-Holt) quantum circuit based on Alice and Bob's input bits.
    
    Args:
        alice (int): Alice's input bit (0 or 1)
        bob (int): Bob's input bit (0 or 1)
        
    Returns:
        QuantumCircuit: The constructed quantum circuit for CHSH experiment
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)
    
    # Prepare entangled state |phi+> = (|00> + |11>)/sqrt(2)
    qc.h(0)  # Apply Hadamard to first qubit
    qc.cx(0, 1)  # Apply CNOT with first as control and second as target
    
    # Alice's measurement basis choice
    if alice == 0:
        # Use computational basis (no rotation needed)
        pass
    elif alice == 1:
        # Use diagonal basis (apply rotation before measurement)
        qc.ry(-1 * 0.5 * 3.141592653589793, 0)  # Rotate -π/2 around Y-axis
    
    # Bob's measurement basis choice
    if bob == 0:
        # Use computational basis (no rotation needed)
        pass
    elif bob == 1:
        # Use diagonal basis (apply rotation before measurement)
        qc.ry(-0.5 * 3.141592653589793, 1)  # Rotate -π/2 around Y-axis
    
    # Measure both qubits
    qc.measure(0, 0)  # Measure Alice's qubit
    qc.measure(1, 1)  # Measure Bob's qubit
    
    return qc
