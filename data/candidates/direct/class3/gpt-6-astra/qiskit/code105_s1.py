# EVAL_META: task_id=105, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral


def initialize_cnot_dihedral():
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    circuit.t(0)
    return CNOTDihedral(circuit)
