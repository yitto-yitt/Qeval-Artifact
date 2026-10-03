# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)

    # Step 1: Rotate q0 so that P(|1>) = 1/3, P(|0>) = 2/3
    theta = 2 * np.arcsin(1 / np.sqrt(3))
    qc.ry(theta, 0)

    # Step 2: Flip q0 to control on |0> state
    qc.x(0)

    # Step 3: Controlled-Hadamard on q1 (controlled by q0) via decomposition
    # CH = Ry(pi/4) . CX . Ry(-pi/4) on target
    qc.ry(np.pi / 4, 1)
    qc.cx(0, 1)
    qc.ry(-np.pi / 4, 1)

    # Step 4: Toffoli to handle the |11> -> |111> component
    qc.ccx(0, 1, 2)

    # Step 5: CX to flip q2 when q0=1
    qc.cx(0, 2)

    # Step 6: Flip q0 back
    qc.x(0)

    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc
