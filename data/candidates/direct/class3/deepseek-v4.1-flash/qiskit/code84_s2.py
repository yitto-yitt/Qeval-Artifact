# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate

def controlled_custom_unitary_circuit():
    qc = QuantumCircuit(2)
    custom_gate = UGate(0.3, 0.2, 0.1)
    qc.append(custom_gate.control(), [0, 1])
    return qc
