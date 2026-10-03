# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

def circ_to_gate(circ):
    qubits = sorted(circ.all_qubits())
    unitary = cirq.unitary(circ, qubit_order=qubits)
    return cirq.MatrixGate(unitary)
