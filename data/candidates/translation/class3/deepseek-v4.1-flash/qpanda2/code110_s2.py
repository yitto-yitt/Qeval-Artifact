# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)

def equivalent_clifford_circuit(circuit, n):
    circ_qubits = circuit.get_qubits()
    num_qubits = len(circ_qubits)
    
    results = []
    for _ in range(n):
        seq = []
        for _ in range(20 * num_qubits):
            op = random.choice(['H', 'S', 'CNOT'])
            if op == 'H':
                q = random.randint(0, num_qubits - 1)
                seq.append(('H', q))
            elif op == 'S':
                q = random.randint(0, num_qubits - 1)
                seq.append(('S', q))
            else:
                if num_qubits < 2:
                    continue
                c = random.randint(0, num_qubits - 1)
                t = random.randint(0, num_qubits - 1)
                while t == c:
                    t = random.randint(0, num_qubits - 1)
                seq.append(('CNOT', c, t))
        
        R = QCircuit()
        for op in seq:
            if op[0] == 'H':
                R << H(circ_qubits[op[1]])
            elif op[0] == 'S':
                R << S(circ_qubits[op[1]])
            else:
                R << CNOT(circ_qubits[op[1]], circ_qubits[op[2]])
        
        R_inv = QCircuit()
        for op in reversed(seq):
            if op[0] == 'H':
                R_inv << H(circ_qubits[op[1]])
            elif op[0] == 'S':
                R_inv << S(circ_qubits[op[1]])
                R_inv << S(circ_qubits[op[1]])
                R_inv << S(circ_qubits[op[1]])
            else:
                R_inv << CNOT(circ_qubits[op[1]], circ_qubits[op[2]])
        
        new_circ = QCircuit()
        new_circ << circuit
        new_circ << R
        new_circ << R_inv
        results.append(new_circ)
    
    return results

machine.finalize()
