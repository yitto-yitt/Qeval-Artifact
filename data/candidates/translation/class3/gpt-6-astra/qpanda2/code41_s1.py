# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, X, Y, I

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    try:
        program = QProg()
        program << X(qubits[0]) << I(qubits[1]) << Y(qubits[2])

        operator = np.empty((8, 8), dtype=complex)
        for column in range(8):
            state = np.zeros(8, dtype=complex)
            state[column] = 1.0
            machine.init_state(state.tolist())
            machine.directly_run(program)
            operator[:, column] = np.asarray(machine.get_qstate(), dtype=complex)

        return operator
    finally:
        machine.finalize()
