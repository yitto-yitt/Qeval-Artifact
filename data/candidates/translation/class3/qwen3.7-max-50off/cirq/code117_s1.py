# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    unitary = np.array(unitary, dtype=complex)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, unitary, allow_partial_czs=False)
    
    circuit = cirq.Circuit()
    for op in ops:
        if hasattr(op, 'gate') and isinstance(op.gate, cirq.CZPowGate) and op.gate.exponent == 1:
            circuit.append(cirq.H(op.qubits[1]))
            circuit.append(cirq.CNOT(op.qubits[0], op.qubits[1]))
            circuit.append(cirq.H(op.qubits[1]))
        else:
            circuit.append(op)
            
    return circuit
