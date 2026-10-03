# EVAL_META: task_id=90, framework=qiskit, class=3

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import XGate, HGate


def create_custom_controlled():
    # Create a base 2-qubit gate with X on qubit 0 and H on qubit 1
    base_qr = QuantumRegister(2)
    base_circ = QuantumCircuit(base_qr, name="custom_base")
    base_circ.x(base_qr[0])
    base_circ.h(base_qr[1])
    base_gate = base_circ.to_gate()

    # Create a controlled version with 2 control qubits
    controlled_gate = base_gate.control(2)

    # Create the main 4-qubit circuit
    qr = QuantumRegister(4)
    circuit = QuantumCircuit(qr)

    # Apply the double-controlled gate
    # Controls: qubits 0 and 3, Targets: qubits 1 and 2
    circuit.append(controlled_gate, [qr[0], qr[3], qr[1], qr[2]])

    return circuit
