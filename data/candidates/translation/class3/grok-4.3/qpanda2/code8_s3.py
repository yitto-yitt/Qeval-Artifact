# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(1)
def rx_gate(value=None):
    circuit = QCircuit()
    if value is not None:
        circuit << RX(qubits[0], value)
    else:
        theta = var.create_variable(name="theta")
        circuit << RX(qubits[0], theta)
    return circuit
machine.finalize()
