# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    if not isinstance(bitstring, str) or len(bitstring) != 2:
        raise ValueError("bitstring must be a string of length 2")
    qc = QuantumCircuit(2, 2)
    # Create shared Bell pair
    qc.h(0)
    qc.cx(0, 1)
    # Encode the two classical bits
    b0, b1 = bitstring[0], bitstring[1]
    if b1 == '1':
        qc.x(0)
    if b0 == '1':
        qc.z(0)
    # Decode and measure
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    return qc
