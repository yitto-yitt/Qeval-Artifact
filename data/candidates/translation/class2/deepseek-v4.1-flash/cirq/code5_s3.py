# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q0))
    return circuit
