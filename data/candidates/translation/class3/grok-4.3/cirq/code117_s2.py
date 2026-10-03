# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    decomposer = cirq.TwoQubitBasisDecomposer(cirq.CNOT)
    operations = decomposer(np.asarray(unitary))
    return cirq.Circuit(operations)
