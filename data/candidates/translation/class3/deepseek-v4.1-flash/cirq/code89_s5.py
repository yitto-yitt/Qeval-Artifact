# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.ControlledGate(cirq.H, num_controls=2).on(q0, q1, q2))
    return circuit
