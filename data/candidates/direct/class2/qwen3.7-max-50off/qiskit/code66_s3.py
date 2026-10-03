# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)

    # Step 1: Rotate q0 so that P(|1>) = 1/3
    theta = 2 * np.arcsin(1 / np.sqrt(3))
    qc.ry(theta, 0)

    # Step 2: Controlled-Ry(pi/2) on q1, controlled by q0=|0>
    qc.x(0)
    qc.cry(np.pi / 2, 0, 1)
    qc.x(0)

    # Step 3: Toffoli on q2, controlled by q0=|0> and q1=|0>
    qc.x(0)
    qc.x(1)
    qc.ccx(0, 1, 2)
    qc.x(0)
    qc.x(1)

    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc
