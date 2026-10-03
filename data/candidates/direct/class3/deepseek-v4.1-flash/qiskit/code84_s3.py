# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit

def controlled_custom_unitary_circuit():
    custom = QuantumCircuit(1, name="custom_unitary")
    custom.u(0.3, 0.2, 0.1, 0)

    custom_gate = custom.to_gate()
    controlled_gate = custom_gate.control(1)

    qc = QuantumCircuit(2)
    qc.append(controlled_gate, [0, 1])

    return qc
