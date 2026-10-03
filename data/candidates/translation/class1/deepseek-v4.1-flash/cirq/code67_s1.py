# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
from numpy import pi

def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    if alice == 0:
        circuit.append(cirq.ry(0)(q0))
    else:
        circuit.append(cirq.ry(-pi / 2)(q0))
    circuit.append(cirq.measure(q0, key='0'))
    if bob == 0:
        circuit.append(cirq.ry(-pi / 4)(q1))
    else:
        circuit.append(cirq.ry(pi / 4)(q1))
    circuit.append(cirq.measure(q1, key='1'))
    return circuit
