# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
import scipy.linalg
from pyqpanda3.core import QuantumMachine, QCircuit

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qm = QuantumMachine()
    qubits = qm.alloc_qubits(n)
    
    pauli_map = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    mat = np.array([[1]], dtype=complex)
    for p in pauli_string:
        mat = np.kron(mat, pauli_map[p])
        
    U = scipy.linalg.expm(-1j * time * mat)
    
    circ = QCircuit()
    try:
        circ.unitary(U, qubits)
    except Exception:
        from pyqpanda3.core import gate_factory
        circ << gate_factory.Unitary(U, qubits)
        
    return circ
