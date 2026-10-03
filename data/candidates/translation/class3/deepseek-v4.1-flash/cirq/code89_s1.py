# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q = cirq.LineQubit.range(3)
    gate = cirq.ControlledGate(cirq.H, num_controls=2)
    circuit = cirq.Circuit(gate.on(q[0], q[1], q[2]))
    return circuit
