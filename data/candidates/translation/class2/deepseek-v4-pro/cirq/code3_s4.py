# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.CNOT(q[0], q[2]))
    circuit.append(cirq.measure(q[0]))
    circuit.append(cirq.measure(q[1]))
    circuit.append(cirq.measure(q[2]))

    if drawing:
        return circuit, str(circuit)
    return circuit
