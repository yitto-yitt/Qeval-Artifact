# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    custom_circ = QuantumCircuit(2, name="custom_xh")
    custom_circ.x(0)
    custom_circ.h(1)
    custom_gate = custom_circ.to_gate()
    controlled_gate = custom_gate.control(2)
    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])
    return qc
