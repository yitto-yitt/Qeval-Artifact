# EVAL_META: task_id=5, framework=cirq, class=2
import cirq

def create_state_prep():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.X(q[1]))
    return circuit
