# EVAL_META: task_id=110, framework=qpanda, class=3
import random
from pyqpanda3.core import *

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    qubits = get_all_used_qubits(circuit)
    for _ in range(n):
        prog = QProg()
        prog << circuit
        if qubits:
            k = random.randint(1, 5)
            for _ in range(k):
                q = random.choice(qubits)
                r = random.choice(['H', 'X', 'Y', 'Z'])
                if r == 'H':
                    prog << H(q) << H(q)
                elif r == 'X':
                    prog << X(q) << X(q)
                elif r == 'Y':
                    prog << Y(q) << Y(q)
                elif r == 'Z':
                    prog << Z(q) << Z(q)
        qc_list.append(prog)
    return qc_list
