# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.measure(q[0], key="c0"))
    return circuit
