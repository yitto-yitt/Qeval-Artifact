# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    equivalents = []
    for _ in range(n):
        new_circ = circuit.copy()
        for __ in range(np.random.randint(1, 6)):
            q = np.random.randint(0, num_qubits)
            choice = np.random.choice(["h", "s", "cx"])
            if choice == "h":
                new_circ.h(q)
                new_circ.h(q)
            elif choice == "s":
                for _ in range(4):
                    new_circ.s(q)
            elif choice == "cx" and num_qubits > 1:
                q2 = np.random.randint(0, num_qubits)
                if q != q2:
                    new_circ.cx(q, q2)
                    new_circ.cx(q, q2)
        equivalents.append(new_circ)
    return equivalents
