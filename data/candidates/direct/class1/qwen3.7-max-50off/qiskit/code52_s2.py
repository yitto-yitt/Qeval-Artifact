# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)

    # Create Bell pair (entanglement shared between sender q0 and receiver q1)
    qc.h(0)
    qc.cx(0, 1)

    # Sender encodes two classical bits onto qubit 0
    if bitstring[1] == '1':
        qc.x(0)
    if bitstring[0] == '1':
        qc.z(0)

    # Receiver decodes: Bell basis measurement
    qc.cx(0, 1)
    qc.h(0)

    # Measure both qubits
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
