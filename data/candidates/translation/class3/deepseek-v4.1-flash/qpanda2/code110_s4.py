# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import random

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(10)

def get_unitary(circuit, num_qubits):
    dim = 1 << num_qubits
    mat = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        prog = QProg()
        for j in range(num_qubits):
            if (i >> j) & 1:
                prog << X(global_qubits[j])
        prog << circuit
        machine.run(prog, 0)
        state = machine.get_qstate()
        for k in range(dim):
            mat[k][i] = state[k]
    return mat

def random_clifford_circuit(num_qubits):
    length = 20 * num_qubits
    circ = QCircuit()
    for _ in range(length):
        r = random.random()
        if r < 0.4:
            q = random.randint(0, num_qubits-1)
            circ << H(global_qubits[q])
        elif r < 0.7:
            q = random.randint(0, num_qubits-1)
            circ << S(global_qubits[q])
        else:
            if num_qubits >= 2:
                control = random.randint(0, num_qubits-1)
                target = random.randint(0, num_qubits-1)
                while target == control:
                    target = random.randint(0, num_qubits-1)
                circ << CNOT(global_qubits[control], global_qubits[target])
            else:
                q = random.randint(0, num_qubits-1)
                circ << H(global_qubits[q])
    return circ

def equivalent_clifford_circuit(circuit, n):
    qubits_used = circuit.get_qubits()
    num_qubits = max(q.get_index() for q in qubits_used) + 1
    
    U_orig = get_unitary(circuit, num_qubits)
    
    result = []
    attempts = 0
    max_attempts = 100000
    while len(result) < n and attempts < max_attempts:
        attempts += 1
        rand_circ = random_clifford_circuit(num_qubits)
        U_rand = get_unitary(rand_circ, num_qubits)
        inner = np.vdot(U_orig, U_rand)
        if np.abs(inner) > 1e-12:
            theta = -np.angle(inner)
            if np.allclose(U_orig, np.exp(1j * theta) * U_rand, rtol=0.4, atol=0.4):
                result.append(rand_circ)
    return result

if __name__ == "__main__":
    machine.finalize()
