# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import random

# Global QVM
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def prog_to_matrix(prog):
    qubits = get_all_used_qubits(prog)
    num_qubits = len(qubits)
    mat_flat = get_matrix(prog)
    dim = 1 << num_qubits
    return np.array(mat_flat).reshape((dim, dim))

def is_equivalent(mat1, mat2, rtol=0.4, atol=0.4):
    if mat1.shape != mat2.shape:
        return False
    idx = np.argmax(np.abs(mat1))
    val1 = mat1.flat[idx]
    val2 = mat2.flat[idx]
    if np.abs(val2) < 1e-9:
        return False
    phase = val1 / val2
    diff = np.abs(mat1 - phase * mat2)
    return np.all(diff <= (atol + rtol * np.abs(phase * mat2)))

def get_random_1q_clifford(qubit):
    prog = QProg()
    for _ in range(random.randint(1, 10)):
        gate = random.choice(['H', 'S'])
        if gate == 'H':
            prog << H(qubit)
        else:
            prog << S(qubit)
    return prog

def get_equivalent_by_identity(circuit, qubits):
    prog = QProg()
    prog << circuit
    for _ in range(random.randint(2, 5)):
        identity_type = random.choice(['H', 'S', 'X', 'Y', 'Z', 'CNOT'])
        if identity_type == 'CNOT' and len(qubits) > 1:
            q1, q2 = random.sample(qubits, 2)
            prog << CNOT(q1, q2) << CNOT(q1, q2)
        else:
            q = random.choice(qubits)
            if identity_type == 'H':
                prog << H(q) << H(q)
            elif identity_type == 'S':
                prog << S(q) << S(q) << S(q) << S(q)
            elif identity_type == 'X':
                prog << X(q) << X(q)
            elif identity_type == 'Y':
                prog << Y(q) << Y(q)
            elif identity_type == 'Z':
                prog << Z(q) << Z(q)
    return prog

def equivalent_clifford_circuit(circuit, n):
    qubits = get_all_used_qubits(circuit)
    num_qubits = len(qubits)
    
    if num_qubits == 0:
        return [QProg() for _ in range(n)]
        
    qc_list = []
    
    try:
        target_mat = prog_to_matrix(circuit)
        has_matrix = True
    except:
        has_matrix = False
        
    if num_qubits == 1 and has_matrix:
        counter = 0
        attempts = 0
        while counter < n and attempts < 500:
            attempts += 1
            qc = get_random_1q_clifford(qubits[0])
            try:
                qc_mat = prog_to_matrix(qc)
                if is_equivalent(target_mat, qc_mat):
                    qc_list.append(qc)
                    counter += 1
            except:
                continue
        while len(qc_list) < n:
            qc_list.append(get_equivalent_by_identity(circuit, qubits))
    else:
        for _ in range(n):
            qc_list.append(get_equivalent_by_identity(circuit, qubits))
            
    return qc_list

machine.finalize()
