# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(cirq.unitary(cirq.qis.UGate(np.pi / 2, np.pi / 2, np.pi / 2)))(q))
    return circuit
