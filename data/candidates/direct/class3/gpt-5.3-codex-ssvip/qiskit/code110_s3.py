# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import random


def equivalent_clifford_circuit(circuit, n):
    base = Clifford(circuit)
    num_qubits = circuit.num_qubits
    out = []

    for _ in range(int(n)):
        cand = QuantumCircuit(num_qubits)
        depth = random.randint(max(1, num_qubits), max(2, 6 * num_qubits))
        for _ in range(depth):
            gate_type = random.choice(["h", "s", "sdg", "x", "y", "z", "cx", "cz", "swap"])
            if gate_type in {"h", "s", "sdg", "x", "y", "z"}:
                q = random.randrange(num_qubits)
                getattr(cand, gate_type)(q)
            elif gate_type in {"cx", "cz"} and num_qubits >= 2:
                a, b = random.sample(range(num_qubits), 2)
                getattr(cand, gate_type)(a, b)
            elif gate_type == "swap" and num_qubits >= 2:
                a, b = random.sample(range(num_qubits), 2)
                cand.swap(a, b)

        cand_cl = Clifford(cand)
        eq_cl = cand_cl.adjoint().compose(base)
        eq_circ = eq_cl.to_circuit()
        out.append(cand.compose(eq_circ))

    return out
