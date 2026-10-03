# EVAL_META: task_id=58, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Gate


def create_ch_gate() -> Gate:
    qc = QuantumCircuit(2, name="ch")
    qc.ry(-3.141592653589793 / 4, 1)
    qc.cx(0, 1)
    qc.ry(3.141592653589793 / 4, 1)
    return qc.to_gate(label="ch")
