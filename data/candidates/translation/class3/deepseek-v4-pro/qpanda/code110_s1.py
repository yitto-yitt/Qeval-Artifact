# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import random
from pyqpanda3.core import QCircuit, gate

def equivalent_clifford_circuit(circuit, n):
    qubits = circuit.getQubits()
    num_qubits = len(qubits)
    U = circuit.get_matrix()

    def is_equiv(A, B, rtol=0.4, atol=0.4):
        d = A.shape[0]
        inner = np.trace(np.dot(A.T.conj(), B)) / d
        if abs(inner) < 1e-12:
            return False
        phase = inner / abs(inner)
        return np.allclose(A, phase * B, rtol=rtol, atol=atol)

    qc_list = []
    max_attempts = 2000 * n  # safety cap
    attempts = 0
    while len(qc_list) < n and attempts < max_attempts:
        attempts += 1
        ident = QCircuit()
        for _ in range(random.randint(1, 3 * num_qubits)):
            if random.random() < 0.6:
                q = random.choice(qubits)
                g = random.choice(['H', 'S', 'X', 'Y', 'Z'])
                if g == 'H':
                    ident << gate.H(q)
                    ident << gate.H(q)
                elif g == 'S':
                    ident << gate.S(q)
                    ident << gate.S(q).dagger()
                elif g == 'X':
                    ident << gate.X(q)
                    ident << gate.X(q)
                elif g == 'Y':
                    ident << gate.Y(q)
                    ident << gate.Y(q)
                elif g == 'Z':
                    ident << gate.Z(q)
                    ident << gate.Z(q)
            else:
                c = random.choice(qubits)
                t = random.choice(qubits)
                while t == c:
                    t = random.choice(qubits)
                ident << gate.CNOT(c, t)
                ident << gate.CNOT(c, t)
        new_c = circuit + ident
        V = new_c.get_matrix()
        if is_equiv(U, V):
            qc_list.append(new_c)
    return qc_list
