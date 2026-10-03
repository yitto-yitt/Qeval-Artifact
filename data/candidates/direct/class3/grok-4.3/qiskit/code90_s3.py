# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    base = QuantumCircuit(2, name="custom")
    base.x(0)
    base.h(1)
    base_gate = base.to_gate()
    controlled = base_gate.control(2)
    qc = QuantumCircuit(4)
    qc.append(controlled, [0, 3, 1, 2])
    return qc
