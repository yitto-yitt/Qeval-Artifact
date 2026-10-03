# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate, YGate, ZGate, HGate, CXGate, CZGate, SwapGate

def equivalent_clifford_circuit(circuit: QuantumCircuit, n: int):
    num_qubits = circuit.num_qubits
    equivalent_circuits = []
    
    for _ in range(n):
        new_circ = circuit.copy()
        num_pairs = random.randint(2, 5)
        
        for _ in range(num_pairs):
            if num_qubits >= 2:
                gate_type = random.choice(['x', 'y', 'z', 'h', 'cx', 'cz', 'swap'])
            else:
                gate_type = random.choice(['x', 'y', 'z', 'h'])
                
            if gate_type == 'x':
                q = random.randint(0, num_qubits - 1)
                new_circ.append(XGate(), [q])
                new_circ.append(XGate(), [q])
            elif gate_type == 'y':
                q = random.randint(0, num_qubits - 1)
                new_circ.append(YGate(), [q])
                new_circ.append(YGate(), [q])
            elif gate_type == 'z':
                q = random.randint(0, num_qubits - 1)
                new_circ.append(ZGate(), [q])
                new_circ.append(ZGate(), [q])
            elif gate_type == 'h':
                q = random.randint(0, num_qubits - 1)
                new_circ.append(HGate(), [q])
                new_circ.append(HGate(), [q])
            elif gate_type == 'cx':
                q1, q2 = random.sample(range(num_qubits), 2)
                new_circ.append(CXGate(), [q1, q2])
                new_circ.append(CXGate(), [q1, q2])
            elif gate_type == 'cz':
                q1, q2 = random.sample(range(num_qubits), 2)
                new_circ.append(CZGate(), [q1, q2])
                new_circ.append(CZGate(), [q1, q2])
            elif gate_type == 'swap':
                q1, q2 = random.sample(range(num_qubits), 2)
                new_circ.append(SwapGate(), [q1, q2])
                new_circ.append(SwapGate(), [q1, q2])
                
        equivalent_circuits.append(new_circ)
        
    return equivalent_circuits
