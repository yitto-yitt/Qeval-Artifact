# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    u = np.asarray(unitary, dtype=np.complex128)

    if "matrix_decompose" in globals():
        for args in (([0, 1], u), (u, [0, 1])):
            try:
                return matrix_decompose(*args)
            except Exception:
                pass

    if "unitary_decomposer_nq" in globals():
        for args in ((u, [0, 1]), ([0, 1], u)):
            try:
                return unitary_decomposer_nq(*args)
            except Exception:
                pass

    circ = QCircuit(2)
    if "QOracle" in globals():
        try:
            circ << QOracle(u, [0, 1])
            return circ
        except Exception:
            try:
                circ << QOracle([0, 1], u)
                return circ
            except Exception:
                pass

    if "OracleGate" in globals():
        try:
            circ << OracleGate([0, 1], u)
            return circ
        except Exception:
            try:
                circ << OracleGate(u, [0, 1])
                return circ
            except Exception:
                pass

    raise RuntimeError("No pyQPanda3 unitary decomposition interface is available.")
