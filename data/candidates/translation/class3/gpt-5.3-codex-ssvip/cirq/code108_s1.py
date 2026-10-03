# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    choi1 = cirq.qis.QuantumChannel(np.array(data1, dtype=complex))
    choi2 = cirq.qis.QuantumChannel(np.array(data2, dtype=complex))
    choi1_matrix = np.array(choi1._channel_data, dtype=complex)
    choi2_matrix = np.array(choi2._channel_data, dtype=complex)
    adjoint_choi1 = cirq.qis.QuantumChannel(np.conjugate(choi1_matrix).T)
    composed_choi = cirq.qis.QuantumChannel(choi1_matrix @ choi2_matrix)
    return choi1, adjoint_choi1, composed_choi
