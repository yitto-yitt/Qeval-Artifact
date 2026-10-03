# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq
from cirq.testing import random_clifford_tableau


def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = cirq.num_qubits(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford_tableau(num_qubits).to_circuit()
        op_qc = cirq.unitary(qc)
        if np.allclose(op_qc - op_or, 0, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
