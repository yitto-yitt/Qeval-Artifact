# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append(cirq.S(q1) ** -1)
    circuit.append(cirq.CX(q0, q1))
    circuit.append(cirq.S(q1))
    return circuit
