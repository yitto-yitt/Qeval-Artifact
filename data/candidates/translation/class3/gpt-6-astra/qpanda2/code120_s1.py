# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, QOracle, get_matrix

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(24)


def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")

    size = len(values)
    if size < 2 or size & (size - 1):
        raise ValueError("The number of diagonal entries must be a power of two.")
    if not np.allclose(np.abs(values), 1.0):
        raise ValueError("Every diagonal entry must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    if num_qubits > len(qubits):
        raise ValueError("The diagonal exceeds the allocated quantum register.")

    circuit = QCircuit()
    circuit << QOracle(
        qubits[:num_qubits],
        np.diag(values).reshape(-1).tolist(),
    )

    program = QProg()
    program << circuit
    get_matrix(program)
    return circuit


atexit.register(lambda: machine.finalize())
