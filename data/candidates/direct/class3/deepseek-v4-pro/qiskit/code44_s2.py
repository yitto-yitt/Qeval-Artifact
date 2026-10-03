# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit


def tensor_circuits():
    """Return the tensor product of a 2-qubit CRY circuit and a 1-qubit X circuit."""
    cry_qc = QuantumCircuit(2)
    cry_qc.cry(0.2, 0, 1)

    x_qc = QuantumCircuit(1)
    x_qc.x(0)

    return cry_qc.tensor(x_qc)
