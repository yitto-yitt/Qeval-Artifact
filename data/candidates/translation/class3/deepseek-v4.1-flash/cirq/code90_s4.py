# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    q = cirq.LineQubit.range(4)
    sub_gate = cirq.MatrixGate(np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H)))
    controlled_gate = cirq.ControlledGate(sub_gate, num_controls=2)
    circuit = cirq.Circuit(controlled_gate.on(q[0], q[3], q[1], q[2]))
    return circuit
