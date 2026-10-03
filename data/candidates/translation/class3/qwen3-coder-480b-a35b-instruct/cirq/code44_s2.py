# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    top = cirq.Circuit()
    q_top = cirq.LineQubit(0)
    top.append(cirq.X(q_top))
    
    bottom = cirq.Circuit()
    q_bottom_0 = cirq.LineQubit(1)
    q_bottom_1 = cirq.LineQubit(2)
    bottom.append(cirq.ControlledGate(cirq.ry(0.2)).on(q_bottom_0, q_bottom_1))
    
    # Combine circuits: bottom (2-qubit) before top (1-qubit) in tensor product
    tensored = cirq.Circuit(bottom.all_operations(), top.all_operations())
    
    return tensored
