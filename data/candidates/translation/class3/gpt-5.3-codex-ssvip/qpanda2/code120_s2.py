# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(32)

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    if 2 ** n != len(diag):
        raise ValueError("Length of diag must be a power of 2.")
    if n > len(_global_qubits):
        raise ValueError("Not enough preallocated qubits.")
    qubits = _global_qubits[:n]
    U = np.diag(diag).astype(complex)
    prog = pq.QProg()
    prog.insert(pq.matrix_decompose(qubits, U))
    machine.directly_run(prog)
    machine.finalize()
    return prog
