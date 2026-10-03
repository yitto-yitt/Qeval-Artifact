# EVAL_META: task_id=110, framework=qpanda, class=3
import random
from pyqpanda3.core import QCircuit, H, X, Y, Z, CNOT, SWAP

def equivalent_clifford_circuit(circuit, n):
    qubits = circuit.get_qubits()
    num_qubits = len(qubits)
    if num_qubits == 0:
        return [circuit] * n
    result = []
    for _ in range(n):
        D = QCircuit()
        num_gates = random.randint(1, 20 * max(1, num_qubits))
        for _ in range(num_gates):
            gate_type = random.choice(['H', 'X', 'Y', 'Z', 'CNOT', 'SWAP'])
            if gate_type in ['H', 'X', 'Y', 'Z']:
                q = random.choice(qubits)
                if gate_type == 'H':
                    D << H(q)
                elif gate_type == 'X':
                    D << X(q)
                elif gate_type == 'Y':
                    D << Y(q)
                elif gate_type == 'Z':
                    D << Z(q)
            elif gate_type == 'CNOT':
                if num_qubits < 2:
                    continue
                q1, q2 = random.sample(qubits, 2)
                D << CNOT(q1, q2)
            elif gate_type == 'SWAP':
                if num_qubits < 2:
                    continue
                q1, q2 = random.sample(qubits, 2)
                D << SWAP(q1, q2)
        new_circ = QCircuit()
        new_circ << circuit
        new_circ << D
        new_circ << D.dagger()
        result.append(new_circ)
    return result
