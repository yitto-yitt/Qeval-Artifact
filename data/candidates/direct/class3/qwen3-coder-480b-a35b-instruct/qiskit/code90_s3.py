# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import XGate, HGate

def create_custom_controlled():
    # Create the base 2-qubit gate (X on qubit 0, H on qubit 1)
    base_qc = QuantumCircuit(2)
    base_qc.x(0)
    base_qc.h(1)
    base_gate = base_qc.to_gate()

    # Create a 4-qubit circuit
    qc = QuantumCircuit(4)

    # Add the controlled version of the gate with qubits 0 and 3 as controls
    # and qubits 1 and 2 as targets
    controlled_gate = base_gate.control(2)  # 2 control qubits
    qc.append(controlled_gate, [0, 3, 1, 2])

    return qc
