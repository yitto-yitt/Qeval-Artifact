# EVAL_META: task_id=110, framework=qiskit, class=3

import random
from qiskit import QuantumCircuit

def equivalent_clifford_circuit(circuit: QuantumCircuit, n: int):
    equivalent_circuits = []
    num_qubits = circuit.num_qubits
    
    for _ in range(n):
        if circuit.qregs:
            new_qc = QuantumCircuit(*circuit.qregs, *circuit.cregs) if circuit.cregs else QuantumCircuit(*circuit.qregs)
        else:
            new_qc = QuantumCircuit(num_qubits)
            
        for inst in circuit.data:
            if random.random() < 0.2:
                gate_type = random.choice(['H', 'X', 'Y', 'Z', 'CX', 'CZ', 'S'])
                if gate_type in ['H', 'X', 'Y', 'Z']:
                    q = random.randint(0, num_qubits - 1)
                    getattr(new_qc, gate_type.lower())(q)
                    getattr(new_qc, gate_type.lower())(q)
                elif gate_type == 'S':
                    q = random.randint(0, num_qubits - 1)
                    new_qc.s(q)
                    new_qc.sdg(q)
                elif gate_type in ['CX', 'CZ'] and num_qubits >= 2:
                    q1, q2 = random.sample(range(num_qubits), 2)
                    getattr(new_qc, gate_type.lower())(q1, q2)
                    getattr(new_qc, gate_type.lower())(q1, q2)
            
            if isinstance(inst, tuple):
                new_qc.append(inst[0], inst[1], inst[2])
            else:
                new_qc.append(inst)
                
        # Append some extra identities to ensure randomness even for small/empty circuits
        num_extra = random.randint(1, 5)
        for _ in range(num_extra):
            gate_type = random.choice(['H', 'X', 'Y', 'Z', 'CX', 'CZ', 'S'])
            if gate_type in ['H', 'X', 'Y', 'Z']:
                q = random.randint(0, num_qubits - 1)
                getattr(new_qc, gate_type.lower())(q)
                getattr(new_qc, gate_type.lower())(q)
            elif gate_type == 'S':
                q = random.randint(0, num_qubits - 1)
                new_qc.s(q)
                new_qc.sdg(q)
            elif gate_type in ['CX', 'CZ'] and num_qubits >= 2:
                q1, q2 = random.sample(range(num_qubits), 2)
                getattr(new_qc, gate_type.lower())(q1, q2)
                getattr(new_qc, gate_type.lower())(q1, q2)
                
        equivalent_circuits.append(new_qc)
        
    return equivalent_circuits
