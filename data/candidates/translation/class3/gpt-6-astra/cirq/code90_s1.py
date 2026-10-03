# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    q = cirq.LineQubit.range(4)
    custom = cirq.CircuitOperation(
        cirq.FrozenCircuit(cirq.X(q[1]), cirq.H(q[2]))
    )
    return cirq.Circuit(custom.controlled_by(q[0], q[3]))
