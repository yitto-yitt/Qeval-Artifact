# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import cmath
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(30)
atexit.register(machine.finalize)

def create_diagonal_circuit(diag):
    length = len(diag)
    if length < 1 or (length & (length - 1)) != 0:
        raise ValueError("Diagonal length must be a positive power of 2.")

    num_qubits = length.bit_length() - 1
    if num_qubits > len(_qubits):
        raise ValueError("Not enough globally allocated qubits.")

    prog = QProg()
    if num_qubits == 0:
        return prog

    qubits = _qubits[:num_qubits]
    target = qubits[num_qubits - 1]
    controls = [qubits[i] for i in range(num_qubits - 1)]

    for index, value in enumerate(diag):
        value = complex(value)
        if not math.isclose(abs(value), 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Diagonal entries must have unit magnitude.")

        angle = cmath.phase(value)

        for bit in range(num_qubits):
            if ((index >> bit) & 1) == 0:
                prog.insert(X(qubits[bit]))

        gate = U1(target, angle)
        if controls:
            gate = gate.control(controls)
        prog.insert(gate)

        for bit in range(num_qubits):
            if ((index >> bit) & 1) == 0:
                prog.insert(X(qubits[bit]))

    return prog
