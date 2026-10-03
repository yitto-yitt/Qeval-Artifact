# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    if bitstring[0] == '1':
        qc.z(0)
    if bitstring[1] == '1':
        qc.x(0)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([1, 0], [0, 1])
    return qc
