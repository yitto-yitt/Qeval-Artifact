# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def controlled_custom_unitary_circuit():
    qc = QuantumCircuit(2)
    try:
        qc.cu3(0.3, 0.2, 0.1, 0, 1)
    except AttributeError:
        try:
            qc.cu(0.3, 0.2, 0.1, 0.0, 0, 1)
        except AttributeError:
            import numpy as np
            theta, phi, lam = 0.3, 0.2, 0.1
            u3 = np.array([
                [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
                [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
            ])
            cu3 = np.eye(4, dtype=complex)
            cu3[2:, 2:] = u3
            try:
                qc.unitary(cu3, [0, 1])
            except AttributeError:
                qc.oracle(cu3, [0, 1])
    return qc
