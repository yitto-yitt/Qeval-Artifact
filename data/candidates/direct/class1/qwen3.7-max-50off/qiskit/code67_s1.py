# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit
import numpy as np


def chsh_circuit(alice, bob):
    """Design a CHSH circuit that takes Alice and Bob input bits and returns the measured QuantumCircuit.

    The CHSH game: Alice and Bob share a Bell pair. Based on their input bits,
    they choose measurement bases to maximize the probability that a XOR b == x AND y.

    Optimal quantum strategy:
    - Alice: x=0 -> Z basis, x=1 -> X basis
    - Bob: y=0 -> (Z+X)/sqrt(2) basis, y=1 -> (Z-X)/sqrt(2) basis
    """
    qc = QuantumCircuit(2, 2)

    # Create Bell pair |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement basis rotation (qubit 0)
    if alice == 0:
        # Measure in Z basis (no rotation)
        pass
    elif alice == 1:
        # Measure in X basis
        qc.h(0)

    # Bob's measurement basis rotation (qubit 1)
    if bob == 0:
        # Measure in (Z+X)/sqrt(2) basis: rotate by -pi/4 around Y
        qc.ry(-np.pi / 4, 1)
    elif bob == 1:
        # Measure in (Z-X)/sqrt(2) basis: rotate by pi/4 around Y
        qc.ry(np.pi / 4, 1)

    # Measure both qubits
    qc.measure([0, 1], [0, 1])

    return qc
