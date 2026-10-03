# EVAL_META: task_id=69, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CSGate


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cs(0, 1)
    qc.h(1)
    qc.append(CSGate().inverse(), [1, 0])
    return qc
