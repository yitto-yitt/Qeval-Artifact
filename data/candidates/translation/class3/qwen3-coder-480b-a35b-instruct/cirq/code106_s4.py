# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
from cirq.transformers import compute_cnot_dihedral_from_circuit


def compose_cnot_dihedral():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    
    circ1 = cirq.Circuit()
    circ1.append(cirq.CNOT(qubits[0], qubits[1]))
    circ1.append(cirq.T(qubits[0]))
    elem1 = cirq.qis.CliffordTableau.from_circuit(circ1).to_cnot_dihedral()
    
    circ2 = cirq.Circuit()
    circ2.append(cirq.CNOT(qubits[0], qubits[1]))
    circ2.append(cirq.T(qubits[0]))
    circ2.append(cirq.X(qubits[1]))
    elem2 = cirq.qis.CliffordTableau.from_circuit(circ2).to_cnot_dihedral()
    
    composed_elem = elem1.compose(elem2)
    return composed_elem
