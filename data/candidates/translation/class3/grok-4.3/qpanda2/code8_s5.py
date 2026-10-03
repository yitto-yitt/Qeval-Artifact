# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def rx_gate(value=None):
    theta = Parameter("theta")
    quantum_circuit = QCircuit()
    quantum_circuit << RX(qubits[0], theta)
    if value is not None:
        quantum_circuit = QCircuit()
        quantum_circuit << RX(qubits[0], value)
        return quantum_circuit
    return quantum_circuit
machine.finalize()
