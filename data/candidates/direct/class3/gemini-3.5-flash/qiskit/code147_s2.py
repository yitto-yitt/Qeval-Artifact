# EVAL_META: task_id=147, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate

def mcy(qc: QuantumCircuit) -> QuantumCircuit:
    """Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3."""
    qc.append(YGate().control(4), [0, 1, 2, 3, 4])
    return qc
