# EVAL_META: task_id=120, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal

def create_diagonal_circuit(diag):
    num_qubits = int(np.log2(len(diag)))
    qc = QuantumCircuit(num_qubits)
    diag_gate = Diagonal(diag)
    qc.append(diag_gate, range(num_qubits))
    return qc
