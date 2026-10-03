# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = [cirq.LineQubit(i) for i in range(5)]
    controls = qubits[:4]
    target = qubits[4]
    qc.append(cirq.ControlledGate(cirq.Y, num_controls=4).on(*controls, target))
    return qc
