# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = VariationalQuantumCircuit()

    # First rotation layer: RY, RZ on all qubits
    for i in range(3):
        circuit.insert(VariationalQuantumGate_RY(q[i], var(0.0)))
        circuit.insert(VariationalQuantumGate_RZ(q[i], var(0.0)))

    circuit.insert(BARRIER(q[0], q[1], q[2]))

    # Full entanglement layer for 3 qubits
    circuit.insert(VariationalQuantumGate_CNOT(q[0], q[1]))
    circuit.insert(VariationalQuantumGate_CNOT(q[0], q[2]))
    circuit.insert(VariationalQuantumGate_CNOT(q[1], q[2]))

    circuit.insert(BARRIER(q[0], q[1], q[2]))

    # Final rotation layer: RY, RZ on all qubits
    for i in range(3):
        circuit.insert(VariationalQuantumGate_RY(q[i], var(0.0)))
        circuit.insert(VariationalQuantumGate_RZ(q[i], var(0.0)))

    return circuit

machine.finalize()
