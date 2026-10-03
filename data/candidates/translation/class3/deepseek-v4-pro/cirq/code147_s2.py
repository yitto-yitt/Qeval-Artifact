# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    mcy_op = cirq.Y.controlled(4)
    qc.append(mcy_op(*qubits))
    return qc
