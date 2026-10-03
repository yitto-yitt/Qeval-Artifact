# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import random

# Global QVM: Initialize CPUQVM and qAlloc_many at the global scope.
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(16)

def equivalent_clifford_circuit(circuit, n):
    prog_or = QProg()
    prog_or << circuit
    
    used_qubits = get_all_used_qubits(prog_or)
    if len(used_qubits) == 0:
        used_qubits = [global_qubits[0]]
    else:
        used_qubits.sort(key=lambda q: q.get_phy_addr())
        
    num_qubits = len(used_qubits)
    dim = 1 << num_qubits
    
    mat_or = np.array(get_matrix(prog_or)).reshape((dim, dim))
    
    qc_list = []
    counter = 0
    while counter < n:
        qc = QCircuit()
        num_gates = random.randint(3, 10) * num_qubits
        for _ in range(num_gates):
            gate_type = random.choice(['H', 'S', 'CNOT'])
            if gate_type == 'H':
                q = random.choice(used_qubits)
                qc << H(q)
            elif gate_type == 'S':
                q = random.choice(used_qubits)
                qc << S(q)
            elif gate_type == 'CNOT' and num_qubits > 1:
                q1, q2 = random.sample(used_qubits, 2)
                qc << CNOT(q1, q2)
                
        prog_qc = QProg()
        prog_qc << qc
        mat_qc = np.array(get_matrix(prog_qc)).reshape((dim, dim))
        
        # Check equivalence up to global phase
        val = np.abs(np.trace(np.dot(mat_or.conj().T, mat_qc))) / dim
        if val > 0.95:
            counter += 1
            qc_list.append(qc)
            
    return qc_list

# Manual Cleanup: Always call machine.finalize() at the end of the script.
machine.finalize()
