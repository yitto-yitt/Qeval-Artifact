# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import HamiltonianGate


def synthesize_evolution_gate(pauli_string, time):
    pauli_op = SparsePauliOp.from_list([(pauli_string, 1.0)])
    hamiltonian = pauli_op.to_matrix()
    gate = HamiltonianGate(hamiltonian, time)
    qc = QuantumCircuit(len(pauli_string))
    qc.append(gate, range(len(pauli_string)))
    return qc
