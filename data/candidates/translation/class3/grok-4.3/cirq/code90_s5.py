# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    class CustomGate(cirq.Gate):
        def _num_qubits_(self):
            return 2
        def _decompose_(self, qubits):
            q0, q1 = qubits
            return [cirq.X(q0), cirq.H(q1)]
    custom = CustomGate()
    controlled_custom = custom.controlled(2)
    qc = cirq.Circuit()
    q = cirq.LineQubit.range(4)
    qc.append(controlled_custom.on(q[0], q[3], q[1], q[2]))
    return qc
