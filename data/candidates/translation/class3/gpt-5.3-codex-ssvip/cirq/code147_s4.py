# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    if len(qubits) < 5:
        raise ValueError("Circuit must contain at least 5 qubits.")
    qc.append(cirq.Y(qubits[4]).controlled_by(*qubits[0:4]))
    return qc
