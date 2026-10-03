# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import random

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    for _ in range(n):
        prog = QProg()
        prog.insert(circuit)
        
        qubits = []
        try:
            qubits = get_all_used_qubits(prog)
        except:
            try:
                get_all_used_qubits(prog, qubits)
            except:
                pass
                
        if qubits:
            for _ in range(random.randint(2, 6)):
                q = random.choice(qubits)
                gate_type = random.choice(['H', 'X', 'Y', 'Z', 'S', 'CNOT'])
                if gate_type == 'H':
                    prog.insert(H(q))
                    prog.insert(H(q))
                elif gate_type == 'X':
                    prog.insert(X(q))
                    prog.insert(X(q))
                elif gate_type == 'Y':
                    prog.insert(Y(q))
                    prog.insert(Y(q))
                elif gate_type == 'Z':
                    prog.insert(Z(q))
                    prog.insert(Z(q))
                elif gate_type == 'S':
                    prog.insert(S(q))
                    prog.insert(S(q))
                    prog.insert(S(q))
                    prog.insert(S(q))
                elif gate_type == 'CNOT' and len(qubits) >= 2:
                    q2 = random.choice([x for x in qubits if x != q])
                    prog.insert(CNOT(q, q2))
                    prog.insert(CNOT(q, q2))
        qc_list.append(prog)
    return qc_list
