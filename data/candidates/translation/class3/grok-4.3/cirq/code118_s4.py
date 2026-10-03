# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qc = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    c3sx_gate = cirq.SX.controlled(3)
    qc.append(c3sx_gate.on(*qubits))
    return qc
