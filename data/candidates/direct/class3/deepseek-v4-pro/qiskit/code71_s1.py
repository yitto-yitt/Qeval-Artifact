# EVAL_META: task_id=71, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit.library import SXGate


def create_quantum_circuit_based_h0_csx01_h1():
    """Create a 3-qubit circuit with H on q0, controlled-SX (control q0, target q1), and H on q1."""
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.append(SXGate().control(1), [0, 1])
    qc.h(1)
    return qc
