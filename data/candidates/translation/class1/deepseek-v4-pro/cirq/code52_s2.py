# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    measure = cirq.NamedQubit.range(2, prefix="measure")

    circuit = cirq.Circuit()
    circuit.append(cirq.H(sender))
    circuit.append(cirq.CX(sender, receiver))
    circuit.append(cirq.Moment())
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))
    circuit.append(cirq.Moment())
    circuit.append(cirq.CX(sender, receiver))
    circuit.append(cirq.H(sender))
    circuit.append(cirq.measure(sender, key="measure_0"))
    circuit.append(cirq.measure(receiver, key="measure_1"))

    return circuit
