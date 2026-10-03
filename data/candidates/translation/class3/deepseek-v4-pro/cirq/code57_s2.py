# EVAL_META: task_id=57, framework=cirq, class=3
import cirq

def create_swap_gate():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[0]),
        cirq.CNOT(q[0], q[1]),
    )
    return circuit
