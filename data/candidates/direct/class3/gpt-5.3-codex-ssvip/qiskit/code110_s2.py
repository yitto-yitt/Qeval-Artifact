# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import random

def equivalent_clifford_circuit(circuit, n):
    base = Clifford(circuit)
    num_qubits = circuit.num_qubits
    out = []
    max_tries = max(50, 20 * n)
    tries = 0

    while len(out) < n and tries < max_tries:
        tries += 1
        rand_cl = Clifford.random(num_qubits, seed=random.randint(0, 2**32 - 1))
        candidate = rand_cl.compose(base).compose(rand_cl.adjoint())
        qc = candidate.to_circuit()
        if Clifford(qc) == base:
            out.append(qc)

    while len(out) < n:
        out.append(base.to_circuit())

    return out
