# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    """Design a CHSH circuit that takes Alice and Bob input bits.

    Creates a Bell pair and applies measurement basis rotations based on
    Alice's and Bob's input bits, then measures both qubits.

    Optimal CHSH strategy:
      Alice: x=0 -> Z basis, x=1 -> X basis
      Bob:   y=0 -> (Z+X)/sqrt(2) basis, y=1 -> (Z-X)/sqrt(2) basis

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

    # Alice's measurement basis rotation on qubit 0
    if alice == 0:
        pass  # Z basis (no rotation)
    else:
        qc.ry(-np.pi / 2, 0)  # X basis

    # Bob's measurement basis rotation on qubit 1
    if bob == 0:
        qc.ry(-np.pi / 4, 1)  # (Z+X)/sqrt(2) basis
    else:
        qc.ry(np.pi / 4, 1)   # (Z-X)/sqrt(2) basis

    # Measure both qubits
    qc.measure([0, 1], [0, 1])

    return qc
