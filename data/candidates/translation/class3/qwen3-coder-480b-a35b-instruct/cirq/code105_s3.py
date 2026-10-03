# EVAL_META: task_id=105, framework=cirq, class=3
import cirq
from cirq import ops


def initialize_cnot_dihedral():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.T(qubits[0]))
    
    # In Cirq, we don't have a direct equivalent to Qiskit's CNOTDihedral,
    # but we can return the circuit which represents the same operation
    return circuit
