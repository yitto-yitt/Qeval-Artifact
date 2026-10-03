# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    q = cirq.LineQubit.range(4)
    subcircuit = cirq.Circuit(cirq.X(q[1]), cirq.H(q[2]))
    custom = cirq.CircuitOperation(cirq.FrozenCircuit(subcircuit))
    controlled_custom = custom.controlled_by(q[0], q[3])
    circuit = cirq.Circuit(controlled_custom)
    return circuit
