# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    circuit = VariationalQuantumCircuit()
    theta = var(0.0 if value is None else float(value), value is None)
    circuit.insert(VariationalQuantumGate_RX(qubits[0], theta))
    return circuit

atexit.register(machine.finalize)
