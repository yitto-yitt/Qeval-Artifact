# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(cirq.unitary(cirq.PhasedXZGate.from_zyz_angles(np.pi / 2, np.pi / 2, np.pi / 2))).on(q))
    return circuit
