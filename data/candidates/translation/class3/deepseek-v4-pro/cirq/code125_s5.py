# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    unitary = cirq.unitary(circ)
    num_qubits = len(circ.all_qubits()) if hasattr(circ, 'all_qubits') else len(circ.qid_shape())
    gate = cirq.MatrixGate(unitary, qid_shape=(2,) * num_qubits)
    return gate
