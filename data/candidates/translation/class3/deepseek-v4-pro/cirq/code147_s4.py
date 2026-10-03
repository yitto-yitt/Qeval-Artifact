# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = sorted(qc.all_qubits())
    ctrl_qubits = qubits[:4]
    target_qubit = qubits[4]
    qc.append(cirq.Y.controlled(len(ctrl_qubits)).on(*ctrl_qubits, target_qubit))
    return qc
