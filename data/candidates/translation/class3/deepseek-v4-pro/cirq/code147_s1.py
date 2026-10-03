# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    controls = qubits[:4]
    target = qubits[4]
    op = cirq.Y.controlled(4).on(*controls, target)
    return qc + cirq.Circuit(op)
