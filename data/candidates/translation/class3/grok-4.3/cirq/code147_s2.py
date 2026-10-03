# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    mcy_gate = cirq.ControlledGate(cirq.Y, num_controls=4)
    qc.append(mcy_gate.on(*cirq.LineQubit.range(5)))
    return qc
