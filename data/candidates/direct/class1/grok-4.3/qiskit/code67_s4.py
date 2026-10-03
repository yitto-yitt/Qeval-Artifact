# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    theta_a = 0 if alice == 0 else np.pi / 2
    theta_b = np.pi / 4 if bob == 0 else -np.pi / 4
    qc.ry(-theta_a, 0)
    qc.ry(-theta_b, 1)
    qc.measure([0, 1], [0, 1])
    return qc
