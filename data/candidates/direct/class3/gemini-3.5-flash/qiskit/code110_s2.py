# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit

def equivalent_clifford_circuit(circuit, n):
    circuits = []
    num_qubits = circuit.num_qubits
    
    if num_qubits == 0:
        return [circuit.copy() for _ in range(n)]
        
    for _ in range(n):
        qc = circuit.copy()
        num_insertions = random.randint(5, 15)
        for _ in range(num_insertions):
            gate_type = random.choice(['H', 'S', 'CX', 'X', 'Y', 'Z', 'Sdg'])
            if gate_type == 'H':
                q = random.randint(0, num_qubits - 1)
                qc.h(q)
                qc.h(q)
            elif gate_type == 'S':
                q = random.randint(0, num_qubits - 1)
                qc.s(q)
                qc.sdg(q)
            elif gate_type == 'Sdg':
                q = random.randint(0, num_qubits - 1)
                qc.sdg(q)
                qc.s(q)
            elif gate_type == 'X':
                q = random.randint(0, num_qubits - 1)
                qc.x(q)
                qc.x(q)
            elif gate_type == 'Y':
                q = random.randint(0, num_qubits - 1)
                qc.y(q)
                qc.y(q)
            elif gate_type == 'Z':
                q = random.randint(0, num_qubits - 1)
                qc.z(q)
                qc.z(q)
            elif gate_type == 'CX' and num_qubits >= 2:
                q1, q2 = random.sample(range(num_qubits), 2)
                qc.cx(q1, q2)
                qc.cx(q1, q2)
        circuits.append(qc)
    return circuits
