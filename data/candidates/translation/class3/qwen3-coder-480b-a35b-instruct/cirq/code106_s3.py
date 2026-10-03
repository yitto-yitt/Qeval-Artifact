# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
from cirq import Circuit


def compose_cnot_dihedral():
    # Create first circuit
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circ1 = Circuit()
    circ1.append(cirq.CNOT(qubits[0], qubits[1]))
    circ1.append(cirq.T(qubits[0]))
    
    # Create second circuit (same as first but with additional X gate on qubit 1)
    circ2 = Circuit()
    circ2.append(cirq.CNOT(qubits[0], qubits[1]))
    circ2.append(cirq.T(qubits[0]))
    circ2.append(cirq.X(qubits[1]))
    
    # Since Cirq doesn't have CNOTDihedral, we return the composed circuit directly
    # This is a conceptual translation - in actual Cirq usage, you would work with circuits directly
    composed_circuit = circ1 + circ2
    
    return composed_circuit
