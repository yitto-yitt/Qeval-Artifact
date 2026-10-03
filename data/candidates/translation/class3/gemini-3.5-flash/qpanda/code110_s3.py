# EVAL_META: task_id=110, framework=qpanda, class=3
import random
import pyqpanda3.core as pq

def equivalent_clifford_circuit(circuit, n):
    qubits = pq.get_all_used_qubits(circuit)
    qc_list = []
    
    if not qubits:
        for _ in range(n):
            prog = pq.QProg()
            prog << circuit
            qc_list.append(prog)
        return qc_list

    for _ in range(n):
        prog = pq.QProg()
        prog << circuit
        
        num_blocks = random.randint(1, 5)
        for _ in range(num_blocks):
            gate_type = random.choice(['H', 'X', 'Y', 'Z', 'CNOT'])
            if gate_type == 'CNOT' and len(qubits) >= 2:
                q1, q2 = random.sample(qubits, 2)
                prog << pq.CNOT(q1, q2) << pq.CNOT(q1, q2)
            else:
                q = random.choice(qubits)
                if gate_type == 'H':
                    prog << pq.H(q) << pq.H(q)
                elif gate_type == 'X':
                    prog << pq.X(q) << pq.X(q)
                elif gate_type == 'Y':
                    prog << pq.Y(q) << pq.Y(q)
                elif gate_type == 'Z':
                    prog << pq.Z(q) << pq.Z(q)
                    
        qc_list.append(prog)
        
    return qc_list
