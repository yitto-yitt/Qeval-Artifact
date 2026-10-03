# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    bits = str(bitstring)
    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("bitstring must be a two-character string containing only '0' and '1'")

    qc = QuantumCircuit(2, 2)

    qc.h(0)
    qc.cx(0, 1)

    if bits[0] == "1":
        qc.z(0)
    if bits[1] == "1":
        qc.x(0)

    qc.cx(0, 1)
    qc.h(0)

    qc.measure(0, 1)
    qc.measure(1, 0)

    return qc
