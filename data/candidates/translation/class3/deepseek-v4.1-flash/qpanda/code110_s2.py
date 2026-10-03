# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import random
from pyqpanda3.core import QCircuit, QProg, Hadamard, CNOT, Phase, get_unitary

def equivalent_clifford_circuit(circuit, n):
    def get_unitary_of_circuit(c):
        if isinstance(c, QCircuit):
            prog = QProg()
            prog << c
            return get_unitary(prog)
        else:
            return get_unitary(c)

    def random_clifford_circuit(num_qubits):
        circ = QCircuit()
        depth = random.randint(50, 200)
        for _ in range(depth):
            if num_qubits == 1:
                gate_type = random.choice(['H', 'S'])
            else:
                gate_type = random.choice(['H', 'S', 'CNOT'])
            if gate_type == 'H':
                q = random.randint(0, num_qubits - 1)
                circ << Hadamard(q)
            elif gate_type == 'S':
                q = random.randint(0, num_qubits - 1)
                circ << Phase(q, np.pi / 2)
            elif gate_type == 'CNOT':
                c = random.randint(0, num_qubits - 1)
                t = random.randint(0, num_qubits - 1)
                while t == c:
                    t = random.randint(0, num_qubits - 1)
                circ << CNOT(c, t)
        return circ

    def is_equivalent(u1, u2, rtol=0.4, atol=0.4):
        dim = u1.shape[0]
        overlap = np.trace(u1.conj().T @ u2) / dim
        if np.abs(overlap) < 1e-10:
            return False
        phase = overlap / np.abs(overlap)
        return np.allclose(u1, u2 * phase, rtol=rtol, atol=atol)

    op_or = get_unitary_of_circuit(circuit)
    num_qubits = int(np.log2(op_or.shape[0]))
    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford_circuit(num_qubits)
        op_qc = get_unitary_of_circuit(qc)
        if is_equivalent(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
