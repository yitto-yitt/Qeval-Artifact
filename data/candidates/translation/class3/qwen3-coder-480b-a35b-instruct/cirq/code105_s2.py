# EVAL_META: task_id=105, framework=cirq, class=3
import cirq
from cirq.contrib.acquaintance import CNOTDihedral


def initialize_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.T(q0))
    elem = CNOTDihedral.from_circuit(circuit)
    return elem
