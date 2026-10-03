# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    sub = QuantumCircuit(2, name="custom")
    sub.x(0)
    sub.h(1)
    gate = sub.to_gate()
    controlled_gate = gate.control(2)

    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])
    return qc
