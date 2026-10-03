# EVAL_META: task_id=105, framework=cirq, class=3
import cirq

def initialize_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.CNOT(q0, q1),
        cirq.T(q0)
    ])
    return circuit
