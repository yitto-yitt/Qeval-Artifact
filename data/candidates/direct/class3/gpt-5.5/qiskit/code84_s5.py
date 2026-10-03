# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate


def controlled_custom_unitary_circuit():
    circuit = QuantumCircuit(2)
    custom_unitary = UGate(0.3, 0.2, 0.1)
    controlled_gate = custom_unitary.control(1)
    circuit.append(controlled_gate, [0, 1])
    return circuit
