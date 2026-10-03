# EVAL_META: task_id=10, framework=cirq, class=3
import cirq

def create_operator():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.X.on_each(*q))
    return circuit
