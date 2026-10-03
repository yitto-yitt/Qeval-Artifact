# EVAL_META: task_id=38, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CRZGate, CRYGate


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.append(CRZGate(theta), [0, 1])
    qc.h(1)
    qc.append(CRYGate(theta), [1, 0])
    return qc
