# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, RX

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    circuit = QCircuit()
    angle = value if value is not None else 0.0
    circuit << RX(qubits[0], angle)
    return circuit

if __name__ == "__main__":
    machine.finalize()
