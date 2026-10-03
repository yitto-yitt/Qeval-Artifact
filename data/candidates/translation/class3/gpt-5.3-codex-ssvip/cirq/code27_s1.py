# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    q = [cirq.NamedQubit(f"q[{i}]") for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.H(q[0]))
    return circuit
