# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    if len(qubits) < 5:
        existing = set(qubits)
        idx = 0
        while len(qubits) < 5:
            q = cirq.LineQubit(idx)
            if q not in existing:
                qubits.append(q)
            idx += 1
        qubits = sorted(qubits)
    controls = qubits[:4]
    target = qubits[4]
    qc.append(cirq.Y(target).controlled_by(*controls))
    return qc
