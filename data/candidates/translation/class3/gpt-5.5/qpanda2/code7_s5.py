# EVAL_META: task_id=7, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def create_parametrized_gate():
    theta = pq.var(np.array([0.0], dtype=float), True)
    quantum_circuit = pq.VariationalQuantumCircuit()
    quantum_circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))
    return quantum_circuit


atexit.register(machine.finalize)
