# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if not isinstance(bitstring, str) or len(bitstring) != 2 or any(
        bit not in "01" for bit in bitstring
    ):
        raise ValueError("bitstring must be a two-character binary string.")

    circuit = QuantumCircuit(2, 2)

    # Share a Bell pair: qubit 0 belongs to the sender, qubit 1 to the receiver.
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.barrier()

    # Encode both classical bits on the sender's qubit.
    if bitstring[1] == "1":
        circuit.x(0)
    if bitstring[0] == "1":
        circuit.z(0)
    circuit.barrier()

    # Transmit qubit 0 and decode at the receiver.
    circuit.cx(0, 1)
    circuit.h(0)

    # Qiskit displays classical strings as c1 c0.
    circuit.measure(0, 1)
    circuit.measure(1, 0)

    return circuit
