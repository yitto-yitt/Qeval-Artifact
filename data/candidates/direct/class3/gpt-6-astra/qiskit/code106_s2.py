# EVAL_META: task_id=106, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral


def compose_cnot_dihedral():
    first = QuantumCircuit(2)
    first.cx(0, 1)
    first.t(0)

    second = QuantumCircuit(2)
    second.cx(0, 1)
    second.t(0)
    second.x(1)

    return CNOTDihedral(first).compose(CNOTDihedral(second)).to_circuit()
