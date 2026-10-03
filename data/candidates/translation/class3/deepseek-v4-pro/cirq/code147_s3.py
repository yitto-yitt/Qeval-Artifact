# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    gate = cirq.Y.controlled(4)
    qc.append(gate(*qubits[:5]))
    return qc
