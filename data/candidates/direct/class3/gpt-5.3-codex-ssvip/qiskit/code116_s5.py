# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit.circuit.library import HamiltonianGate


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    pauli_op = Pauli(pauli_string).to_matrix()
    hamiltonian = 0.5 * pauli_op
    gate = HamiltonianGate(hamiltonian, time)
    qc = QuantumCircuit(n)
    qc.append(gate, range(n))
    return qc
