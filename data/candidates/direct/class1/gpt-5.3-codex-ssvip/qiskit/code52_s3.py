# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if not isinstance(bitstring, str) or len(bitstring) != 2 or any(b not in "01" for b in bitstring):
        raise ValueError("bitstring must be a 2-character string containing only '0' and '1'.")

    qc = QuantumCircuit(2, 2)

    # Create shared Bell pair between sender (q0) and receiver (q1)
    qc.h(0)
    qc.cx(0, 1)

    # Sender encodes two classical bits on one qubit (superdense coding)
    b0, b1 = bitstring[0], bitstring[1]
    if b1 == "1":
        qc.x(0)
    if b0 == "1":
        qc.z(0)

    # Receiver decodes
    qc.cx(0, 1)
    qc.h(0)

    # Measure both qubits to recover the two bits
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
