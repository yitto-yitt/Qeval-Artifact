# EVAL_META: task_id=41, framework=cirq, class=3
import cirq


def compose_op():
    identity = cirq.DensePauliString('III')
    yx = cirq.DensePauliString('YX')
    qargs = [0, 2]

    expanded_paulis = ['I'] * 3
    for qarg, pauli in zip(qargs, yx.pauli_mask):
        expanded_paulis[qarg] = pauli

    return cirq.DensePauliString(''.join(expanded_paulis))
