# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1 or diagonal.size < 2:
        raise ValueError("diag must be a one-dimensional sequence of length 2**n.")
    size = int(diagonal.size)
    if size & (size - 1):
        raise ValueError("The length of diag must be a power of two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("Every diagonal entry must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    if num_qubits > len(qubits):
        raise ValueError("The diagonal exceeds the available qubit capacity.")

    matrix = np.diag(diagonal).ravel().tolist()
    circuit = pq.QCircuit()
    circuit << pq.QOracle(qubits[:num_qubits], matrix)

    program = pq.QProg()
    program << circuit
    pq.get_matrix(program)
    return circuit


atexit.register(lambda: machine.finalize())
