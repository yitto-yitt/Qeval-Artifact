# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    """
    Creates a CHSH (Clauser-Horne-Shimony-Holt) quantum circuit based on Alice's and Bob's input bits.

    Args:
        alice (int): Alice's input bit (0 or 1)
        bob (int): Bob's input bit (0 or 1)

    Returns:
        QuantumCircuit: The quantum circuit implementing the CHSH game strategy
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Prepare entangled Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement basis choice
    if alice == 0:
        # Measurement in Z basis (no rotation needed)
        pass
    elif alice == 1:
        # Measurement in X basis (Hadamard before measurement)
        qc.h(0)

    # Bob's measurement basis choice
    if bob == 0:
        # Measurement in Z basis rotated by -π/8
        qc.rz(-1 * 3.14159 / 8, 1)
        qc.h(1)
    elif bob == 1:
        # Measurement in X basis rotated by π/8
        qc.rz(3.14159 / 8, 1)
        qc.h(1)

    # Measure both qubits
    qc.measure_all()

    return qc
