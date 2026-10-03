# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    q0, q1, q2, q3 = cirq.LineQubit.range(4)
    sub_gate = cirq.MatrixGate(np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H)))
    controlled_gate = cirq.ControlledGate(sub_gate, num_controls=2)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(q0, q3, q1, q2))
    return circuit
