# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    top = cirq.Circuit(cirq.X(cirq.LineQubit(0)))
    bottom = cirq.Circuit(cirq.ControlledGate(cirq.ry(0.2)).on(cirq.LineQubit(0), cirq.LineQubit(1)))
    tensored = cirq.Circuit(bottom.all_qubits(), top.all_qubits())
    tensored.append(bottom.all_operations())
    tensored.append(top.all_operations())
    return tensored
