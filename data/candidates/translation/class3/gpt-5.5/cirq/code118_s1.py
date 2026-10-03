# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    c3sx_op = cirq.XPowGate(exponent=0.5).on(qubits[3]).controlled_by(qubits[0], qubits[1], qubits[2])
    return cirq.Circuit(c3sx_op)
