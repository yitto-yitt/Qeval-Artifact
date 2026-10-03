# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import random

def equivalent_clifford_circuit(circuit, n):
    prog = QProg()
    prog.insert(circuit)
    qubits = get_all_used_qubits(prog)
    
    qc_list = []
    for _ in range(n):
        new_prog = QProg()
        new_prog.insert(circuit)
        
        if len(qubits) > 0:
            for _ in range(random.randint(1, 3)):
                q = random.choice(qubits)
                gate_type = random.choice(['H', 'S', 'X', 'Y', 'Z'])
                if gate_type == 'H':
                    new_prog.insert(H(q))
                    new_prog.insert(H(q))
                elif gate_type == 'S':
                    for _ in range(4):
                        new_prog.insert(S(q))
                elif gate_type == 'X':
                    new_prog.insert(X(q))
                    new_prog.insert(X(q))
                elif gate_type == 'Y':
                    new_prog.insert(Y(q))
                    new_prog.insert(Y(q))
                elif gate_type == 'Z':
                    new_prog.insert(Z(q))
                    new_prog.insert(Z(q))
        qc_list.append(new_prog)
    return qc_list
