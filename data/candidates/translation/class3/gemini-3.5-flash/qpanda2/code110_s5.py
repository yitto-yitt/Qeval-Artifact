# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(20)

def equivalent_clifford_circuit(circuit, n):
    used_qubits = get_all_used_qubits(circuit)
    if not used_qubits:
        used_qubits = [q[0]]
    
    qc_list = []
    for i in range(n):
        new_prog = QProg()
        new_prog.insert(circuit)
        
        num_identities = random.randint(1, 5)
        for _ in range(num_identities):
            opt = random.choice(['H', 'S', 'X', 'Y', 'Z', 'CNOT'])
            if opt == 'CNOT' and len(used_qubits) >= 2:
                q1, q2 = random.sample(used_qubits, 2)
                new_prog.insert(CNOT(q1, q2))
                new_prog.insert(CNOT(q1, q2))
            else:
                qubit = random.choice(used_qubits)
                if opt == 'H':
                    new_prog.insert(H(qubit))
                    new_prog.insert(H(qubit))
                elif opt == 'S':
                    for _ in range(4):
                        new_prog.insert(S(qubit))
                elif opt == 'X':
                    new_prog.insert(X(qubit))
                    new_prog.insert(X(qubit))
                elif opt == 'Y':
                    new_prog.insert(Y(qubit))
                    new_prog.insert(Y(qubit))
                elif opt == 'Z':
                    new_prog.insert(Z(qubit))
                    new_prog.insert(Z(qubit))
        qc_list.append(new_prog)
    return qc_list

machine.finalize()
