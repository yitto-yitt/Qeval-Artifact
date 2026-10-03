# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit
import numpy as np


def chsh_circuit(alice, bob):
    """
    Design a CHSH circuit that takes Alice and Bob input bits and returns
    the measured QuantumCircuit.

    The CHSH game: Alice and Bob share a Bell pair. Based on their input bits
    (alice, bob), they choose measurement bases to maximize the probability
    that a XOR b == alice AND bob.

    Optimal quantum strategy:
      - Alice x=0: measure Z (angle 0)
      - Alice x=1: measure X (angle pi/2)
      - Bob y=0: measure (Z+X)/sqrt(2) (angle pi/4)
      - Bob y=1: measure (Z-X)/sqrt(2) (angle -pi/4)

    Args:
        alice (int): Alice's input bit (0 or 1).
        bob (int): Bob's input bit (0 or 1).

    Returns:
        QuantumCircuit: The measured CHSH circuit.
    """
    qc = QuantumCircuit(2, 2)

    # Create Bell pair |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement basis rotation
    if alice == 1:
        # Measure in X basis (rotate by pi/2 in XZ plane)
        qc.h(0)

    # Bob's measurement basis rotation
    if bob == 0:
        # Measure (Z+X)/sqrt(2): rotate by -pi/4 around Y, then measure Z
        qc.ry(-np.pi / 4, 1)
    else:
        # Measure (Z-X)/sqrt(2): rotate by pi/4 around Y, then measure Z
        qc.ry(np.pi / 4, 1)

    # Measure both qubits
    qc.measure([0, 1], [0, 1])

    return qc
