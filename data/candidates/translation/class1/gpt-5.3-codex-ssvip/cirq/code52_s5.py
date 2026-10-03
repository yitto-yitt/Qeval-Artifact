# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    c0 = cirq.NamedQubit("measure_0")
    c1 = cirq.NamedQubit("measure_1")

    circuit = cirq.Circuit()
    circuit.append(cirq.H(sender))
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.Moment())  # barrier equivalent

    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))

    circuit.append(cirq.Moment())  # barrier equivalent
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.H(sender))
    circuit.append(cirq.measure(sender, key="measure_0"))
    circuit.append(cirq.measure(receiver, key="measure_1"))
    return circuit
