# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    mat = np.array(unitary, dtype=np.complex128)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, mat, allow_partial_czs=False)
    
    new_ops = []
    for op in ops:
        if op.gate == cirq.CZ:
            new_ops.append(cirq.H(op.qubits[1]))
            new_ops.append(cirq.CNOT(op.qubits[0], op.qubits[1]))
            new_ops.append(cirq.H(op.qubits[1]))
        else:
            new_ops.append(op)
            
    return cirq.Circuit(new_ops)
