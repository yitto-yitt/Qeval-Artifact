# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)

    # Prepare Bell pair |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement basis choice (qubit 0)
    if alice == 0:
        pass  # Measure in Z basis (angle 0)
    elif alice == 1:
        qc.h(0)  # Measure in X basis (angle pi/2)

    # Bob's measurement basis choice (qubit 1)
    if bob == 0:
        qc.ry(-np.pi / 4, 1)  # Measure at angle pi/4 in XZ plane
    elif bob == 1:
        qc.ry(np.pi / 4, 1)   # Measure at angle -pi/4 in XZ plane

    # Measure both qubits
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
