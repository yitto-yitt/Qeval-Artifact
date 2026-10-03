# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit


def tensor_circuits():
    # 1-qubit circuit with an X gate
    x_qc = QuantumCircuit(1)
    x_qc.x(0)

    # 2-qubit circuit with a CRY gate controlled by qubit 0
    cry_qc = QuantumCircuit(2)
    cry_qc.cry(0.2, 0, 1)

    # Tensor product: 2-qubit CRY circuit before 1-qubit X circuit
    combined = cry_qc.tensor(x_qc)
    return combined
