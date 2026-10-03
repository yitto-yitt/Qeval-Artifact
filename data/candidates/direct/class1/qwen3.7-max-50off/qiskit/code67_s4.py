# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    """Design a CHSH circuit that takes Alice and Bob input bits and returns the measured QuantumCircuit."""
    # Optimal CHSH measurement angles
    alice_angles = [0.0, np.pi / 4]
    bob_angles = [np.pi / 8, -np.pi / 8]

    theta_a = alice_angles[int(alice)]
    theta_b = bob_angles[int(bob)]

    qc = QuantumCircuit(2, 2)

    # Create Bell pair |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement basis rotation and measurement
    qc.ry(-2 * theta_a, 0)
    qc.measure(0, 0)

    # Bob's measurement basis rotation and measurement
    qc.ry(-2 * theta_b, 1)
    qc.measure(1, 1)

    return qc
