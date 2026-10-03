# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    measure = cirq.NamedQubit.range(2, prefix="measure")

    circuit = cirq.Circuit()

    # Entanglement preparation
    circuit.append(cirq.H(sender))
    circuit.append(cirq.CNOT(sender, receiver))

    # Encoding based on bitstring
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))

    # Bell measurement
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.H(sender))

    # Measurements
    circuit.append(cirq.measure(sender, key="m0"))
    circuit.append(cirq.measure(receiver, key="m1"))

    return circuit
