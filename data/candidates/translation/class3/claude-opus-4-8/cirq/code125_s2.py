# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    unitary = cirq.unitary(circ)
    num_qubits = len(cirq.QubitOrder.DEFAULT.order_for(circ.all_qubits()))
    return cirq.MatrixGate(unitary, num_qubits=num_qubits)
