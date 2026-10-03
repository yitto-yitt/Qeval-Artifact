# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, RX

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    if value is None:
        theta = 0.0
    else:
        theta = value
    circuit = QCircuit()
    circuit << RX(qubits[0], theta)
    return circuit

machine.finalize()
