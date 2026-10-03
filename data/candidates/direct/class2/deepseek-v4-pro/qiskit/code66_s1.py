# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    """Return a 3-qubit W-state circuit with measurement."""
    qc = QuantumCircuit(3, 3)
    # rotation to set amplitudes on q0
    theta = 2 * np.arcsin(1 / np.sqrt(3))
    qc.ry(theta, 0)
    # entangle q1, q2 conditioned on q0=0 (via temporary X flip)
    qc.x(0)
    qc.cx(0, 2)
    qc.ch(0, 1)
    qc.cx(1, 2)
    qc.x(0)
    # measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
