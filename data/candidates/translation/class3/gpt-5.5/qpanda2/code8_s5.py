# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    if value is None:
        theta = var(np.array([0.0]), True)
        circuit = VariationalQuantumCircuit()
        circuit.insert(VariationalQuantumGate_RX(qubits[0], theta))
        return circuit

    circuit = QCircuit()
    circuit.insert(RX(qubits[0], float(value)))
    return circuit

atexit.register(lambda: machine.finalize())
