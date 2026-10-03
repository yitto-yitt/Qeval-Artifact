# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
import numpy as np

def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    if alice == 0:
        circuit.append(cirq.ry(0).on(q0))
    else:
        circuit.append(cirq.ry(-np.pi / 2).on(q0))
    circuit.append(cirq.measure(q0, key='0'))
    if bob == 0:
        circuit.append(cirq.ry(-np.pi / 4).on(q1))
    else:
        circuit.append(cirq.ry(np.pi / 4).on(q1))
    circuit.append(cirq.measure(q1, key='1'))
    return circuit
