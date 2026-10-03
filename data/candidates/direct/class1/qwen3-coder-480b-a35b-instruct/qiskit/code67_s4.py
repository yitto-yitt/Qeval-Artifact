# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    """
    Creates a CHSH (Clauser-Horne-Shimony-Holt) quantum circuit based on Alice's and Bob's input bits.

    Args:
        alice (int): Alice's input bit (0 or 1)
        bob (int): Bob's input bit (0 or 1)

    Returns:
        QuantumCircuit: The quantum circuit implementing the CHSH game protocol.
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Prepare initial entangled state |Phi+> = (|00> + |11>)/sqrt(2)
    qc.h(0)  # Apply Hadamard gate to qubit 0
    qc.cx(0, 1)  # Apply CNOT gate from qubit 0 to qubit 1

    # Alice's measurement basis choice
    if alice == 0:
        # Measuring in Z basis (no additional rotation needed before measurement)
        pass
    elif alice == 1:
        # Measuring in X basis (rotate by -π/8 from computational basis)
        qc.ry(-1 * 0.5 * 3.14159 / 2, 0)  # RY(-π/4)

    # Bob's measurement basis choice
    if bob == 0:
        # Measuring in Z basis rotated by π/8
        qc.ry(0.5 * 3.14159 / 2, 1)  # RY(π/4)
    elif bob == 1:
        # Measuring in X basis (no additional rotation needed before measurement)
        pass

    # Perform measurements
    qc.measure(0, 0)  # Measure qubit 0 into classical bit 0
    qc.measure(1, 1)  # Measure qubit 1 into classical bit 1

    return qc
