# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    try:
        program = pq.QProg()
        program << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])

        columns = []
        for index in range(4):
            state = [0j] * 4
            state[index] = 1.0 + 0j
            machine.init_state(state)
            machine.directly_run(program)
            columns.append(np.array(machine.get_qstate(), dtype=complex))

        return np.column_stack(columns)
    finally:
        machine.finalize()
