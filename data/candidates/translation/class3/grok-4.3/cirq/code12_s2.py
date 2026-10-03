# EVAL_META: task_id=12, framework=cirq, class=3
import cirq

def get_unitary():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q[0]), cirq.CNOT(q[0], q[1]))
    return cirq.unitary(circuit)
