# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
from cirq.contrib.acquaintance import CNOTDihedralElement


def compose_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)
    
    # Create first circuit: CX(0,1) followed by T(0)
    circ1 = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.T(qubits[0])
    )
    
    # Create second circuit: same as first plus X(1)
    circ2 = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.T(qubits[0]),
        cirq.X(qubits[1])
    )
    
    # Convert to CNOTDihedral elements
    elem1 = CNOTDihedralElement.from_circuit(circ1)
    elem2 = CNOTDihedralElement.from_circuit(circ2)
    
    # Compose the elements
    composed_elem = elem1.then(elem2)
    
    return composed_elem
