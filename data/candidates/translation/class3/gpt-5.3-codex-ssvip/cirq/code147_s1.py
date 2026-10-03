# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    controls = qubits[:4]
    target = qubits[4]
    qc.append(cirq.Y(target).controlled_by(*controls))
    return qc
