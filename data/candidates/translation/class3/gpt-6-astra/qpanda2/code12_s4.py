# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, X, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    try:
        columns = []
        for basis in range(4):
            program = QProg()
            for index in range(2):
                if basis & (1 << index):
                    program << X(qubits[index])
            program << H(qubits[0])
            program << CNOT(qubits[0], qubits[1])
            machine.directly_run(program)
            columns.append(np.asarray(machine.get_qstate(), dtype=complex))
        return np.column_stack(columns)
    finally:
        machine.finalize()
