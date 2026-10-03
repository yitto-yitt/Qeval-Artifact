# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    qc.append(cirq.Y.controlled(4).on(*qubits[:5]))
    return qc
