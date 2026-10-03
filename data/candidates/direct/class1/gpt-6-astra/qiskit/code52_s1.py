# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    if bitstring not in ("00", "01", "10", "11"):
        raise ValueError("bitstring must be '00', '01', '10', or '11'.")

    circuit = QuantumCircuit(2, 2)

    circuit.h(0)
    circuit.cx(0, 1)

    if bitstring[1] == "1":
        circuit.x(0)
    if bitstring[0] == "1":
        circuit.z(0)

    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 1)
    circuit.measure(1, 0)

    return circuit
