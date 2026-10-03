# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import *


def qft_inverse(n):
    circuit = QCircuit()

    def _append(gate):
        nonlocal circuit
        circuit << gate

    def _append_phase(target, angle):
        if "P" in globals():
            _append(P(target, angle))
        elif "U1" in globals():
            _append(U1(target, angle))
        else:
            _append(RZ(target, angle))

    def _append_cnot(control, target):
        if "CNOT" in globals():
            _append(CNOT(control, target))
        else:
            _append(X(target).control([control]))

    def _append_cp(control, target, angle):
        if "CP" in globals():
            try:
                _append(CP(control, target, angle))
                return
            except TypeError:
                try:
                    _append(CP(angle, control, target))
                    return
                except TypeError:
                    pass

        if "CR" in globals():
            try:
                _append(CR(control, target, angle))
                return
            except TypeError:
                pass

        if "P" in globals():
            try:
                _append(P(target, angle).control([control]))
                return
            except TypeError:
                pass

        _append_phase(control, angle / 2.0)
        _append_phase(target, angle / 2.0)
        _append_cnot(control, target)
        _append_phase(target, -angle / 2.0)
        _append_cnot(control, target)

    def _append_swap(a, b):
        if "SWAP" in globals():
            _append(SWAP(a, b))
        else:
            _append_cnot(a, b)
            _append_cnot(b, a)
            _append_cnot(a, b)

    for i in range(n // 2):
        _append_swap(i, n - i - 1)

    for j in range(n):
        for k in range(j):
            _append_cp(j, k, -math.pi / (2 ** (j - k)))
        _append(H(j))

    return circuit
