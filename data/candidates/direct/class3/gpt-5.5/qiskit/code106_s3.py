# EVAL_META: task_id=106, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral


def compose_cnot_dihedral():
    circuit1 = QuantumCircuit(2)
    circuit1.cx(0, 1)
    circuit1.t(0)

    circuit2 = QuantumCircuit(2)
    circuit2.cx(0, 1)
    circuit2.t(0)
    circuit2.x(1)

    dihedral1 = CNOTDihedral(circuit1)
    dihedral2 = CNOTDihedral(circuit2)

    return dihedral1.compose(dihedral2).to_circuit()
