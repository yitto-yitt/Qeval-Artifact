# EVAL_META: task_id=110, framework=qpanda, class=3
import random
from pyqpanda3.core import QCircuit, H, X, Y, Z, CNOT, CZ, SWAP

def equivalent_clifford_circuit(circuit, n):
    qubits = circuit.qubits()
    if not qubits:
        return [QCircuit() for _ in range(n)]
    result = []
    for _ in range(n):
        qc = QCircuit()
        qc << circuit
        seq = []
        for _ in range(10):
            gate_type = random.choice(['H', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'SWAP'])
            if gate_type in ['H', 'X', 'Y', 'Z']:
                q = random.choice(qubits)
                seq.append((gate_type, (q,)))
            else:
                q1, q2 = random.sample(qubits, 2)
                seq.append((gate_type, (q1, q2)))
        for gate_type, qs in seq:
            if gate_type == 'H':
                qc << H(qs[0])
            elif gate_type == 'X':
                qc << X(qs[0])
            elif gate_type == 'Y':
                qc << Y(qs[0])
            elif gate_type == 'Z':
                qc << Z(qs[0])
            elif gate_type == 'CNOT':
                qc << CNOT(qs[0], qs[1])
            elif gate_type == 'CZ':
                qc << CZ(qs[0], qs[1])
            elif gate_type == 'SWAP':
                qc << SWAP(qs[0], qs[1])
        for gate_type, qs in reversed(seq):
            if gate_type == 'H':
                qc << H(qs[0])
            elif gate_type == 'X':
                qc << X(qs[0])
            elif gate_type == 'Y':
                qc << Y(qs[0])
            elif gate_type == 'Z':
                qc << Z(qs[0])
            elif gate_type == 'CNOT':
                qc << CNOT(qs[0], qs[1])
            elif gate_type == 'CZ':
                qc << CZ(qs[0], qs[1])
            elif gate_type == 'SWAP':
                qc << SWAP(qs[0], qs[1])
        result.append(qc)
    return result
