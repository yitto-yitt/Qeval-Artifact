# EVAL_META: task_id=12, framework=cirq, class=3
import cirq


def get_unitary():
    q1, q0 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    return cirq.unitary(circuit)
