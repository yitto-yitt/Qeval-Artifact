# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    bitstring = str(bitstring)
    if len(bitstring) != 2 or any(bit not in "01" for bit in bitstring):
        raise ValueError("bitstring must be a two-character string containing only '0' and '1'.")

    qc = QuantumCircuit(2, 2)

    qc.h(0)
    qc.cx(0, 1)

    if bitstring[1] == "1":
        qc.x(0)
    if bitstring[0] == "1":
        qc.z(0)

    qc.cx(0, 1)
    qc.h(0)

    qc.measure(0, 1)
    qc.measure(1, 0)

    return qc
