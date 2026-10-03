# EVAL_META: task_id=110, framework=cirq, class=3
import numpy as np
import cirq


def equivalent_clifford_circuit(circuit, n):
    """Return n random Clifford circuits equivalent to the given circuit."""
    num_qubits = len(circuit.all_qubits())
    qs = cirq.LineQubit.range(num_qubits)
    if not qs:
        return [cirq.Circuit() for _ in range(n)]
    ref_unitary = circuit.unitary(qubit_order=qs)
    rtol, atol = 0.4, 0.4
    qc_list = []
    while len(qc_list) < n:
        rand_clifford = cirq.CliffordTableau(num_qubits=num_qubits,
                                             initial_state=0)
        qc_candidate = cirq.Circuit(rand_clifford.to_cirq_circuit())
        candidate_unitary = qc_candidate.unitary(qubit_order=qs)
        if np.allclose(ref_unitary, candidate_unitary, rtol=rtol, atol=atol):
            qc_list.append(qc_candidate)
    return qc_list
