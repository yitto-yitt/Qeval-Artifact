# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, RX

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def rx_gate(value=None):
    if value is None:
        theta = "theta"
        circuit = QCircuit()
        circuit.insert(RX(qubits[0], theta))
        return circuit
    circuit = QCircuit()
    circuit.insert(RX(qubits[0], value))
    return circuit


if __name__ == "__main__":
    try:
        prog_unbound = rx_gate()
        prog_bound = rx_gate(0.5)
        print(prog_unbound)
        print(prog_bound)
    finally:
        machine.finalize()
