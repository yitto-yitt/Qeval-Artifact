# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
from cirq import value


def compose_cnot_dihedral():
    # Create two circuits with 2 qubits each
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    
    circ1 = cirq.Circuit()
    circ1.append(cirq.CNOT(qubits[0], qubits[1]))
    circ1.append(cirq.T(qubits[0]))
    
    # Convert to CNOTDihedral - in Cirq we work with operations directly
    elem1 = cirq.DiagramInfo(circ1) if hasattr(cirq, 'DiagramInfo') else circ1
    
    # Second circuit is same as first but with additional X gate on qubit 1
    circ2 = cirq.Circuit()
    circ2.append(cirq.CNOT(qubits[0], qubits[1]))
    circ2.append(cirq.T(qubits[0]))
    circ2.append(cirq.X(qubits[1]))
    
    elem2 = cirq.DiagramInfo(circ2) if hasattr(cirq, 'DiagramInfo') else circ2
    
    # Since Cirq doesn't have direct CNOTDihedral composition like Qiskit,
    # we need to work with the operations/circuits directly
    # However, based on the task requirements, we need to return something equivalent
    # Let's create a combined circuit that represents the composition
    composed_circuit = cirq.Circuit()
    composed_circuit.append(circ1.all_qubits())
    composed_circuit.append(circ2.all_qubits())
    
    # Actually append the operations from both circuits
    composed_circuit = cirq.Circuit(circ1 + circ2)
    
    return composed_circuit
