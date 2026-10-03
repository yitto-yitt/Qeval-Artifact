# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, H, X, Z, CNOT, measure


def send_bits(bitstring):
    circuit = QProg()
    circuit << H(0)
    circuit << CNOT(0, 1)

    if bitstring[1] == "1":
        circuit << Z(0)
    if bitstring[0] == "1":
        circuit << X(0)

    circuit << CNOT(0, 1)
    circuit << H(0)
    circuit << measure([0, 1], [0, 1])

    simulator = CPUQVM()
    simulator.run(circuit, 1)
    return circuit
