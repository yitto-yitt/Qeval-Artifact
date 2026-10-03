# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def send_bits(bitstring):
    sender = QuantumRegister(1, "sender")
    receiver = QuantumRegister(1, "receiver")
    measure = ClassicalRegister(2, "measure")
    circuit = QuantumCircuit(sender, receiver, measure)
    circuit.h(sender)
    circuit.cx(sender, receiver)
    circuit.barrier()
    if bitstring[1] == "1":
        circuit.z(sender)
    if bitstring[0] == "1":
        circuit.x(sender)
    circuit.barrier()
    circuit.cx(sender, receiver)
    circuit.h(sender)
    circuit.measure(sender, measure[0])
    circuit.measure(receiver, measure[1])
    return circuit
