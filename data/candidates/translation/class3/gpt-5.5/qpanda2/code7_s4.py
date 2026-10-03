# EVAL_META: task_id=7, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import CPUQVM, VariationalQuantumCircuit, VariationalQuantumGate_RX, var

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)

def create_parametrized_gate():
    theta = var(np.array([0.0]), True)
    quantum_circuit = VariationalQuantumCircuit()
    quantum_circuit.insert(VariationalQuantumGate_RX(qubits[0], theta[0]))
    return quantum_circuit
