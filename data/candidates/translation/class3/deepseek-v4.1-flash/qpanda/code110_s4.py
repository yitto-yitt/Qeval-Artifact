# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, S, X, Y, Z, CNOT, CZ, get_unitary

def equivalent_clifford_circuit(circuit, n):
    u_in = get_unitary(circuit)
    num_qubits = int(np.log2(u_in.shape[0]))
    
    def random_clifford_circuit(num_qubits):
        circ = QCircuit()
        length = np.random.randint(5, 20)
        for _ in range(length):
            gate_type = np.random.choice(['H', 'S', 'X', 'Y', 'Z', 'CNOT', 'CZ'])
            if gate_type == 'H':
                q = np.random.randint(0, num_qubits)
                circ << H(q)
            elif gate_type == 'S':
                q = np.random.randint(0, num_qubits)
                circ << S(q)
            elif gate_type == 'X':
                q = np.random.randint(0, num_qubits)
                circ << X(q)
            elif gate_type == 'Y':
                q = np.random.randint(0, num_qubits)
                circ << Y(q)
            elif gate_type == 'Z':
                q = np.random.randint(0, num_qubits)
                circ << Z(q)
            elif gate_type == 'CNOT':
                if num_qubits >= 2:
                    q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                    circ << CNOT(q1, q2)
            elif gate_type == 'CZ':
                if num_qubits >= 2:
                    q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                    circ << CZ(q1, q2)
        return circ

    def equiv(u, v, rtol=0.4, atol=0.4):
        idx = np.unravel_index(np.argmax(np.abs(v) > 1e-10), v.shape)
        if np.abs(v[idx]) < 1e-10:
            return np.allclose(u, v, rtol=rtol, atol=atol)
        phase = u[idx] / v[idx]
        return np.allclose(u, phase * v, rtol=rtol, atol=atol)

    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford_circuit(num_qubits)
        u_qc = get_unitary(qc)
        if equiv(u_qc, u_in, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
