# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)

    # Create shared entanglement (Bell pair)
    qc.h(0)
    qc.cx(0, 1)

    # Sender (Alice) encodes two classical bits on her qubit (qubit 0)
    # bitstring[1] (LSB) maps to Z gate
    # bitstring[0] (MSB) maps to X gate
    if bitstring[1] == '1':
        qc.z(0)
    if bitstring[0] == '1':
        qc.x(0)

    # Receiver (Bob) decodes via Bell measurement
    qc.cx(0, 1)
    qc.h(0)

    # Measure both qubits
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
