# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit
import math


def w_state():
    qc = QuantumCircuit(3, 3)
    amp = 1 / math.sqrt(3)
    qc.initialize([0, amp, amp, 0, amp, 0, 0, 0], [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
