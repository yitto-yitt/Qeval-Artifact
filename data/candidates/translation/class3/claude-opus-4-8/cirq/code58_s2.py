# EVAL_META: task_id=58, framework=cirq, class=3
import cirq
from numpy import pi

def create_ch_gate():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(pi/4).on(q[1]))
    circuit.append(cirq.CX(q[0], q[1]))
    circuit.append(cirq.ry(-pi/4).on(q[1]))
    return circuit
