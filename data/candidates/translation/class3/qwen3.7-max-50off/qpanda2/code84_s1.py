# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    cos = np.cos(theta / 2)
    sin = np.sin(theta / 2)
    u3_matrix = np.array([
        [cos, -np.exp(1j * lam) * sin],
        [np.exp(1j * phi) * sin, np.exp(1j * (phi + lam)) * cos]
    ], dtype=complex)
    
    cu3_matrix = np.eye(4, dtype=complex)
    cu3_matrix[2:, 2:] = u3_matrix
    
    circ = pq.QCircuit()
    circ.insert(pq.QOracle(qubits, cu3_matrix))
    return circ

machine.finalize()
