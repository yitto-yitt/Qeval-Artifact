# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
from cirq import value


def compose_cnot_dihedral():
    # Create first circuit
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circ1 = cirq.Circuit()
    circ1.append(cirq.CNOT(qubits[0], qubits[1]))
    circ1.append(cirq.T(qubits[0]))
    
    # Convert to CNOTDihedral (using cirq's representation)
    elem1 = value.CircuitDiagramInfo(circ1)
    
    # Create second circuit (same as first but with additional X gate on qubit 1)
    circ2 = cirq.Circuit()
    circ2.append(cirq.CNOT(qubits[0], qubits[1]))
    circ2.append(cirq.T(qubits[0]))
    circ2.append(cirq.X(qubits[1]))
    
    # Convert to CNOTDihedral
    elem2 = value.CircuitDiagramInfo(circ2)
    
    # Since Cirq doesn't have direct CNOTDihedral composition like Qiskit,
    # we need to work with the circuits directly
    composed_circuit = cirq.Circuit(circ1.all_qubits())
    composed_circuit.append(circ1.all_operations())
    composed_circuit.append(circ2.all_operations())
    
    # Return the composed circuit as a CNOTDihedral equivalent
    # In Cirq, we represent this as a circuit with the operations combined
    return composed_circuit
