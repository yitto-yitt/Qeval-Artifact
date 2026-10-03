# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    measure = cirq.NamedQubit("measure0"), cirq.NamedQubit("measure1")

    circuit = cirq.Circuit()

    circuit.append(cirq.H(sender))
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.Moment())

    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))

    circuit.append(cirq.Moment())
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.H(sender))
    circuit.append(cirq.measure(sender, measure[0]))
    circuit.append(cirq.measure(receiver, measure[1]))

    return circuit
