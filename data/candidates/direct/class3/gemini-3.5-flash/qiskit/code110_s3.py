# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit

def equivalent_clifford_circuit(circuit: QuantumCircuit, n: int):
    num_qubits = circuit.num_qubits
    equivalent_circuits = []
    
    single_qubit_pairs = [
        ('h', 'h'),
        ('s', 'sdg'),
        ('sdg', 's'),
        ('x', 'x'),
        ('y', 'y'),
        ('z', 'z'),
    ]
    
    two_qubit_gates = ['cx', 'cz', 'swap']
    
    for i in range(n):
        qc = circuit.copy()
        num_insertions = random.randint(3, 8)
        for _ in range(num_insertions):
            if num_qubits >= 2 and random.random() < 0.5:
                gate = random.choice(two_qubit_gates)
                q1, q2 = random.sample(range(num_qubits), 2)
                if gate == 'cx':
                    qc.cx(q1, q2)
                    qc.cx(q1, q2)
                elif gate == 'cz':
                    qc.cz(q1, q2)
                    qc.cz(q1, q2)
                elif gate == 'swap':
                    qc.swap(q1, q2)
                    qc.swap(q1, q2)
            else:
                g, g_inv = random.choice(single_qubit_pairs)
                q = random.randint(0, num_qubits - 1)
                getattr(qc, g)(q)
                getattr(qc, g_inv)(q)
        equivalent_circuits.append(qc)
        
    return equivalent_circuits
