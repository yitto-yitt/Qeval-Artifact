# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.NamedQubit("sender")
    receiver = cirq.NamedQubit("receiver")
    circuit = cirq.Circuit()
    circuit.append(cirq.H(sender), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT(sender, receiver), strategy=cirq.InsertStrategy.NEW)
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender), strategy=cirq.InsertStrategy.NEW)
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT(sender, receiver), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.H(sender), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.measure(sender, key="measure_0"), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.measure(receiver, key="measure_1"), strategy=cirq.InsertStrategy.NEW)
    return circuit
