# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit


def send_bits(bitstring):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    if bitstring[1] == "1":
        circuit.z(0)
    if bitstring[0] == "1":
        circuit.x(0)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit
