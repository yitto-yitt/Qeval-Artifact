# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, I, X, Y


def compose_op():
    operator = np.empty((8, 8), dtype=complex)

    for column in range(8):
        program = QProg()
        for qubit in range(3):
            if (column >> qubit) & 1:
                program << X(qubit)

        program << X(0) << I(1) << Y(2)

        simulator = CPUQVM()
        simulator.run(program, 1)
        operator[:, column] = np.asarray(
            simulator.get_state_vector(), dtype=complex
        ).reshape(8)

    return operator
