# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import VariationalQuantumCircuit, var, RY, RZ, CNOT, BARRIER

def create_efficientSU2():
    vqc = VariationalQuantumCircuit()
    q0 = vqc.qAlloc()
    q1 = vqc.qAlloc()
    q2 = vqc.qAlloc()
    qubits = [q0, q1, q2]

    # First rotation layer: Ry, Rz
    for i, q in enumerate(qubits):
        vqc.insert(RY(q, var(f"theta_{i}_ry")))
        vqc.insert(RZ(q, var(f"theta_{i}_rz")))
    vqc.insert(BARRIER(qubits))

    # Entangling layer (full)
    vqc.insert(CNOT(q0, q1))
    vqc.insert(CNOT(q0, q2))
    vqc.insert(CNOT(q1, q2))
    vqc.insert(BARRIER(qubits))

    # Second rotation layer: Ry, Rz
    for i, q in enumerate(qubits):
        vqc.insert(RY(q, var(f"phi_{i}_ry")))
        vqc.insert(RZ(q, var(f"phi_{i}_rz")))
    vqc.insert(BARRIER(qubits))

    return vqc
