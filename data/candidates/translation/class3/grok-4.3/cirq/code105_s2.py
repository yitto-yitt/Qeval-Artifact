# EVAL_META: task_id=105, framework=cirq, class=3
import cirq

def initialize_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)
    circ = cirq.Circuit()
    circ.append(cirq.CNOT(qubits[0], qubits[1]))
    circ.append(cirq.T(qubits[0]))
    return circ
