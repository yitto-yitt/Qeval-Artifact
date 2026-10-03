# EVAL_META: task_id=67, framework=cirq, class=1
import numpy as np
import cirq


def chsh_circuit(alice, bob):
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.CNOT(q[0], q[1]))

    if alice == 0:
        circuit.append(cirq.ry(0)(q[0]))
    else:
        circuit.append(cirq.ry(-np.pi / 2)(q[0]))
    circuit.append(cirq.measure(q[0], key="0"))

    if bob == 0:
        circuit.append(cirq.ry(-np.pi / 4)(q[1]))
    else:
        circuit.append(cirq.ry(np.pi / 4)(q[1]))
    circuit.append(cirq.measure(q[1], key="1"))

    return circuit
