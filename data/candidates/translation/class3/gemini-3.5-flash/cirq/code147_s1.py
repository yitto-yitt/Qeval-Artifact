# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc: cirq.Circuit):
    qubits = sorted(list(qc.all_qubits()))
    if len(qubits) < 5:
        qubits = cirq.LineQubit.range(5)
    
    mcy_gate = cirq.Y.controlled(num_controls=4)
    qc.append(mcy_gate(*qubits[:5]))
    return qc
