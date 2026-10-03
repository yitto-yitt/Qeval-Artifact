# EVAL_META: task_id=110, framework=qpanda, class=3
import random
import numpy as np
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, Y, Z, CNOT, CZ, SWAP

def get_unitary(circuit, num_qubits):
    dim = 1 << num_qubits
    unitary = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        qvm = CPUQVM()
        qvm.init_qvm()
        prog = QProg()
        for q in range(num_qubits):
            if (i >> q) & 1:
                prog << X(q)
        prog << circuit
        qvm.run(prog)
        state = qvm.get_qstate()
        for j in range(dim):
            unitary[j, i] = state[j]
    return unitary

def random_identity_padded_circuit(circuit, num_qubits):
    new_circ = circuit.copy()
    single_gates = [H, X, Y, Z]
    two_gates = [CNOT, CZ, SWAP]
    seq = []
    L = random.randint(1, 10)
    for _ in range(L):
        if random.random() < 0.5 or num_qubits < 2:
            gate = random.choice(single_gates)
            q = random.randint(0, num_qubits - 1)
            seq.append((gate, (q,)))
        else:
            gate = random.choice(two_gates)
            q1 = random.randint(0, num_qubits - 1)
            q2 = random.randint(0, num_qubits - 1)
            while q2 == q1:
                q2 = random.randint(0, num_qubits - 1)
            seq.append((gate, (q1, q2)))
    for gate, args in seq:
        new_circ << gate(*args)
    for gate, args in reversed(seq):
        new_circ << gate(*args)
    return new_circ

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.qubit_num()
    if num_qubits == 0:
        return [QCircuit() for _ in range(n)]
    target_unitary = get_unitary(circuit, num_qubits)
    result = []
    counter = 0
    while counter < n:
        candidate = random_identity_padded_circuit(circuit, num_qubits)
        cand_unitary = get_unitary(candidate, num_qubits)
        inner = np.vdot(cand_unitary, target_unitary)
        if np.abs(inner) > 1e-12:
            phase = inner / np.abs(inner)
        else:
            phase = 1.0
        if np.allclose(target_unitary, phase * cand_unitary, rtol=0.4, atol=0.4):
            counter += 1
            result.append(candidate)
    return result
