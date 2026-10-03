# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate


def controlled_custom_unitary_circuit():
    qc = QuantumCircuit(2)
    custom_u = UGate(0.3, 0.2, 0.1)
    controlled_u = custom_u.control(1)
    qc.append(controlled_u, [0, 1])
    return qc
