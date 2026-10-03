# EVAL_META: task_id=58, framework=cirq, class=3
import cirq
from numpy import pi

def create_ch_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(pi/4).on(q1))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.ry(-pi/4).on(q1))
    return circuit
