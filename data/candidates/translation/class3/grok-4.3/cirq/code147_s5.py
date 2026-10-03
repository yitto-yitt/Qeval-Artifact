# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = cirq.LineQubit.range(5)
    mcy_gate = cirq.Y.controlled(4)
    qc.append(mcy_gate.on(*qubits))
    return qc
