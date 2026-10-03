# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    custom = cirq.MatrixGate(np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H)))
    controlled_custom = cirq.ControlledGate(custom, num_controls=2)
    q = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(controlled_custom(q[0], q[3], q[1], q[2]))
    return circuit
