# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    qubits = sorted(circ.all_qubits())
    unitary = circ.unitary(qubit_order=qubits)
    return cirq.MatrixGate(unitary)
