# EVAL_META: task_id=67, framework=cirq, class=1
import numpy as np
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    c0, c1 = cirq.LineQubit.range(2, 4)  # classical bits are just measurement keys in Cirq
    circuit = cirq.Circuit()

    circuit.append(cirq.H(q0))
    circuit.append(cirq.CX(q0, q1))

    # barrier has no direct equivalent in Cirq; it's a no-op for semantics
    # circuit.append(cirq.Barrier(q0, q1))  # Barrier not needed, skip

    if alice == 0:
        circuit.append(cirq.ry(0)(q0))
    else:
        circuit.append(cirq.ry(-np.pi / 2)(q0))
    circuit.append(cirq.measure(q0, key='c0'))

    if bob == 0:
        circuit.append(cirq.ry(-np.pi / 4)(q1))
    else:
        circuit.append(cirq.ry(np.pi / 4)(q1))
    circuit.append(cirq.measure(q1, key='c1'))

    return circuit
