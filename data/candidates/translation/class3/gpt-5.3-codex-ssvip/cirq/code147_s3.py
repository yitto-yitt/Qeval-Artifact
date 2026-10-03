# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    if len(qubits) < 5:
        raise ValueError("Circuit must contain at least 5 qubits.")
    controls = [qubits[i] for i in range(4)]
    target = qubits[4]
    qc.append(cirq.Y(target).controlled_by(*controls))
    return qc
