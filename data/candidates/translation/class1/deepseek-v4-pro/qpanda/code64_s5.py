# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


_initialized = False


def _ensure_init():
    global _initialized
    if not _initialized:
        init()
        _initialized = True


def simons_algorithm(s):
    _ensure_init()
    n = len(s)
    s = s[::-1]

    q1 = qAlloc_many(n)
    q2 = qAlloc_many(n)
    c = cAlloc_many(n)

    circuit = QCircuit()

    for i in range(n):
        circuit << H(q1[i])

    for i in range(n):
        circuit << CNOT(q1[i], q2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q1[i], q2[j])

    for i in range(n):
        circuit << H(q1[i])

    for i in range(n):
        circuit << Measure(q1[i], c[i])

    return circuit
