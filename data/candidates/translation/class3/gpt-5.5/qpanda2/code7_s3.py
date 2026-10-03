# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = var(0.0, True)
    quantum_circuit = VariationalQuantumCircuit()
    quantum_circuit.insert(VariationalQuantumGate_RX(qubits[0], theta))
    return quantum_circuit

machine.finalize()
