# EVAL_META: task_id=52, framework=cirq, class=1
import cirq

def send_bits(bitstring):
    sender = cirq.LineQubit(0)
    receiver = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(sender))
    circuit.append(cirq.CNOT(sender, receiver))
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.H(sender))
    circuit.append(cirq.measure(sender, receiver, key="result"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    measured = result.measurements["result"][0]
    received = "".join(str(bit) for bit in measured)
    return received
