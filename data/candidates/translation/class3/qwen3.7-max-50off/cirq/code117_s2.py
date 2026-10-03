# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    q0, q1 = cirq.LineQubit.range(2)
    ops = cirq.two_qubit_matrix_to_cz_operations(q0, q1, np.array(unitary))
    
    final_ops = []
    for op in ops:
        if op.gate == cirq.CZ:
            c, t = op.qubits
            final_ops.append(cirq.H(t))
            final_ops.append(cirq.CNOT(c, t))
            final_ops.append(cirq.H(t))
        else:
            final_ops.append(op)
            
    return cirq.Circuit(final_ops)
