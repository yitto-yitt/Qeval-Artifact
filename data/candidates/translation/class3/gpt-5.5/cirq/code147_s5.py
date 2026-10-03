# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(qc.all_qubits()))
    if len(qubits) < 5:
        qubits = cirq.LineQubit.range(5)
    qc.append(cirq.Y(qubits[4]).controlled_by(*qubits[0:4]))
    return qc
