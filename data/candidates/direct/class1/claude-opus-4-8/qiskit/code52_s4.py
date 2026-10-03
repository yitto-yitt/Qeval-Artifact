# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    b0, b1 = bitstring[0], bitstring[1]
    if b1 == '1':
        qc.x(0)
    if b0 == '1':
        qc.z(0)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc
