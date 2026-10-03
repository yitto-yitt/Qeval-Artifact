# EVAL_META: task_id=145, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def qft_inverse(n):
    circuit = pq.QCircuit()

    for i in range(n // 2):
        circuit << pq.SWAP(i, n - i - 1)

    phase_gate = pq.CR if hasattr(pq, "CR") else pq.CP

    for j in range(n):
        for k in range(j - 1, -1, -1):
            circuit << phase_gate(k, j, -math.pi / (2 ** (j - k)))
        circuit << pq.H(j)

    return circuit
