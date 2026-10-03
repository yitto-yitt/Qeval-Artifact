# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = cirq.LineQubit.range(5)
    qc.append(cirq.Y(qubits[4]).controlled_by(*qubits[:4]))
    return qc
