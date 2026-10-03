# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if isinstance(bitstring, (list, tuple)):
        bits = "".join(str(int(b)) if isinstance(b, bool) else str(b) for b in bitstring)
    else:
        bits = str(bitstring).strip()

    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("bitstring must contain exactly two bits")

    circuit = QuantumCircuit(2, 2)

    circuit.h(0)
    circuit.cx(0, 1)

    if bits[0] == "1":
        circuit.z(0)
    if bits[1] == "1":
        circuit.x(0)

    circuit.cx(0, 1)
    circuit.h(0)

    circuit.measure(0, 1)
    circuit.measure(1, 0)

    return circuit
