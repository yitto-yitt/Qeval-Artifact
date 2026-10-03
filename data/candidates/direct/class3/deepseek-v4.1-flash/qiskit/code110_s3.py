# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    results = []
    for _ in range(n):
        qc = circuit.copy()
        if num_qubits == 0:
            results.append(qc)
            continue
        rand_qc = QuantumCircuit(num_qubits)
        for _ in range(random.randint(4, 12)):
            gate = random.choice(['h', 's', 'sdg', 'x', 'y', 'z', 'cx'])
            if gate == 'cx' and num_qubits >= 2:
                c = random.randrange(num_qubits)
                t = random.randrange(num_qubits)
                while t == c:
                    t = random.randrange(num_qubits)
                rand_qc.cx(c, t)
            elif gate != 'cx':
                q = random.randrange(num_qubits)
                getattr(rand_qc, gate)(q)
        qc.compose(rand_qc, inplace=True)
        qc.compose(rand_qc.inverse(), inplace=True)
        results.append(qc)
    return results
