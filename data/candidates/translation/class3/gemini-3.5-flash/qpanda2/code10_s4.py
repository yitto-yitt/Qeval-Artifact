# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_operator():
    matrix = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ], dtype=complex)
    circ = pq.matrix_decompose(q, matrix)
    return circ

if __name__ == "__main__":
    machine.finalize()
