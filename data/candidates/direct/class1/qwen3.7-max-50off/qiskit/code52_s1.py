# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def send_bits(bitstring):
    if isinstance(bitstring, int):
        bitstring = format(bitstring, '02b')
    else:
        bitstring = str(bitstring)

    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # Create shared entanglement (Bell pair)
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes two classical bits onto her qubit (superdense coding)
    if bitstring[1] == '1':
        qc.x(0)
    if bitstring[0] == '1':
        qc.z(0)

    # Bob performs Bell measurement to decode
    qc.cx(0, 1)
    qc.h(0)

    # Measure both qubits
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
