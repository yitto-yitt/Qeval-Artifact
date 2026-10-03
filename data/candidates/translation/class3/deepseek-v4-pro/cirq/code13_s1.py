# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    return cirq.Circuit([
        cirq.rz(lam)(q),
        cirq.ry(theta)(q),
        cirq.rz(phi)(q)
    ])
