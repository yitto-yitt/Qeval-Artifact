# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if isinstance(bitstring, int):
        bits = format(bitstring, "02b")
    else:
        bits = "".join(str(bit) for bit in bitstring)

    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("bitstring must be two classical bits: '00', '01', '10', or '11'")

    qc = QuantumCircuit(2, 2)

    qc.h(0)
    qc.cx(0, 1)

    if bits[1] == "1":
        qc.x(0)
    if bits[0] == "1":
        qc.z(0)

    qc.cx(0, 1)
    qc.h(0)

    qc.measure(0, 1)
    qc.measure(1, 0)

    return qc
