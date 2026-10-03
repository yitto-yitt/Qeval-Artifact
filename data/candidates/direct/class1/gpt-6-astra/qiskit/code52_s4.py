# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if not isinstance(bitstring, str) or bitstring not in ("00", "01", "10", "11"):
        raise ValueError("bitstring must be '00', '01', '10', or '11'.")

    circuit = QuantumCircuit(2, 2)

    # Establish entanglement: sender holds qubit 0, receiver holds qubit 1.
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.barrier()

    # Encode both classical bits on the sender's qubit.
    if bitstring[1] == "1":
        circuit.x(0)
    if bitstring[0] == "1":
        circuit.z(0)
    circuit.barrier()

    # After qubit 0 is transmitted, the receiver decodes both bits.
    circuit.cx(0, 1)
    circuit.h(0)

    # Qiskit displays classical registers most-significant bit first.
    circuit.measure(0, 1)
    circuit.measure(1, 0)

    return circuit
