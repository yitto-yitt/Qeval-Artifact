# EVAL_META: task_id=106, framework=cirq, class=3
import cirq
import numpy as np


def compose_cnot_dihedral():
    # Define qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # First circuit: CX(0,1) followed by T(0)
    circ1 = cirq.Circuit([
        cirq.CNOT(q0, q1),
        cirq.T(q0)
    ])
    
    # Second circuit: same as first but with additional X(1)
    circ2 = cirq.Circuit([
        cirq.CNOT(q0, q1),
        cirq.T(q0),
        cirq.X(q1)
    ])
    
    # Compose the two circuits (first circ1 then circ2)
    composed_circuit = circ1 + circ2
    
    return composed_circuit
