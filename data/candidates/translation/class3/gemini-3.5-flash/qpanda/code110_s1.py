# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import random

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    try:
        qubits = get_all_used_qubits(circuit)
    except Exception:
        qubits = []
        
    for _ in range(n):
        prog = QProg()
        prog.insert(circuit)
        if qubits:
            num_identities = random.randint(1, 5)
            for _ in range(num_identities):
                q = random.choice(qubits)
                gate_type = random.choice(['H', 'X', 'Y', 'Z', 'S4'])
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
                elif gate_type == 'S4':
                    prog.insert(S(q))
                    prog.insert(S(q))
                    prog.insert(S(q))
                    prog.insert(S(q))
        qc_list.append(prog)
    return qc_list
