# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    custom = QuantumCircuit(2, name="custom")
    custom.x(0)
    custom.h(1)
    gate = custom.to_gate()
    controlled_gate = gate.control(2)

    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])
    return qc
