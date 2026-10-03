# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q[0]))
    return circuit
