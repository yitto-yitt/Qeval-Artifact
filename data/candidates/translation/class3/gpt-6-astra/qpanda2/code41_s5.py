# EVAL_META: task_id=41, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    matrix = np.empty((8, 8), dtype=np.complex128)

    for basis in range(8):
        program = pq.QProg()
        for index in range(3):
            if (basis >> index) & 1:
                program << pq.X(qubits[index])

        program << pq.X(qubits[0])
        program << pq.I(qubits[1])
        program << pq.Y(qubits[2])

        machine.directly_run(program)
        matrix[:, basis] = np.asarray(machine.get_qstate(), dtype=np.complex128)

    return matrix


atexit.register(lambda: machine.finalize())
