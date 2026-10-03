# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import cmath
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(20)
atexit.register(machine.finalize)

def create_diagonal_circuit(diag):
    length = len(diag)
    if length == 0 or (length & (length - 1)) != 0:
        raise ValueError("Diagonal length must be a positive power of 2.")

    num_qubits = int(math.log2(length))
    if num_qubits > len(_qubits):
        raise ValueError("Not enough globally allocated qubits.")

    prog = QProg()
    if num_qubits == 0:
        return prog

    qs = _qubits[:num_qubits]

    for basis_index, value in enumerate(diag):
        angle = cmath.phase(complex(value))

        for qubit_index in range(num_qubits):
            if ((basis_index >> qubit_index) & 1) == 0:
                prog << X(qs[qubit_index])

        phase_gate = U1(qs[0], angle)
        if num_qubits > 1:
            phase_gate = phase_gate.control(qs[1:num_qubits])
        prog << phase_gate

        for qubit_index in reversed(range(num_qubits)):
            if ((basis_index >> qubit_index) & 1) == 0:
                prog << X(qs[qubit_index])

    return prog
