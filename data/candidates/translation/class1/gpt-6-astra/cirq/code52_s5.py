# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    circuit = cirq.Circuit(
        cirq.H(sender),
        cirq.CNOT(sender, receiver),
    )
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))
    circuit.append(
        [
            cirq.CNOT(sender, receiver),
            cirq.H(sender),
            cirq.measure(sender, key="measure_0"),
            cirq.measure(receiver, key="measure_1"),
        ]
    )
    return circuit
