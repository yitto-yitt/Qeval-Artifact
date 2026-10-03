# EVAL_META: task_id=10, framework=cirq, class=3
import cirq

def create_operator():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    circuit = cirq.Circuit(cirq.X(q0), cirq.X(q1))
    return circuit
