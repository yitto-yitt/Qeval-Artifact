# EVAL_META: task_id=105, framework=cirq, class=3
import cirq
from cirq import Circuit


def initialize_cnot_dihedral():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = Circuit()
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.T(qubits[0]))
    return circuit
