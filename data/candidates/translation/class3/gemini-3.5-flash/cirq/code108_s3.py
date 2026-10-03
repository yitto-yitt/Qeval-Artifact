# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    # Since Cirq does not have a built-in Choi class with adjoint and compose methods,
    # we represent Choi matrices as numpy arrays and implement the operations.
    # A Choi matrix is a 2D numpy array.
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)

    # Adjoint of a Choi matrix is its conjugate transpose.
    adjoint_choi1 = np.conj(choi1).T

    # Composition of two Choi matrices J1 and J2.
    # For Choi matrices J1 and J2 of channels E1 and E2, the Choi matrix of E2 o E1 is:
    # J_composed = Tr_2 [ (J1^T2 \otimes I) * (I \otimes J2) ]
    # where T2 is the partial transpose on the output space of E1.
    # Assuming data1 and data2 are Choi matrices of d-dimensional systems.
    # Let's determine the dimension d.
    dim_total = choi1.shape[0]
    d = int(np.round(np.sqrt(dim_total)))

    # Reshape J1 to 4D tensor: input1, output1, input2, output2
    # J1 is on A \otimes B. J2 is on B \otimes C.
    # J1 has shape (d, d, d, d)
    J1 = choi1.reshape(d, d, d, d)
    J2 = choi2.reshape(d, d, d, d)

    # We want to compute the composition:
    # J_composed_{a, c, a', c'} = \sum_{b, b'} J1_{a, b, a', b'} * J2_{b, c, b', c'}
    # This corresponds to contracting the output of J1 with the input of J2.
    # In index notation:
    # J_composed[a, c, a', c'] = sum_{b, b'} J1[a, b, a', b'] * J2[b, c, b', c']
    # Let's use np.einsum:
    composed_tensor = np.einsum("abij,bckl->acik", J1, J2)

    # Reshape back to 2D matrix of shape (d^2, d^2)
    composed_choi = composed_tensor.reshape(dim_total, dim_total)

    return choi1, adjoint_choi1, composed_choi
