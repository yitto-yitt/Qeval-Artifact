# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    if len(qubits) < 5:
        qubits = cirq.LineQubit.range(5)
    controls = qubits[0:4]
    target = qubits[4]
    qc.append(cirq.Y(target).controlled_by(*controls))
    return qc
