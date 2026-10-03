# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
from numpy import pi


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT(q0, q1), strategy=cirq.InsertStrategy.NEW)
    if alice == 0:
        circuit.append(cirq.ry(0).on(q0), strategy=cirq.InsertStrategy.NEW)
    else:
        circuit.append(cirq.ry(-pi / 2).on(q0), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.measure(q0, key='0'), strategy=cirq.InsertStrategy.NEW)
    if bob == 0:
        circuit.append(cirq.ry(-pi / 4).on(q1), strategy=cirq.InsertStrategy.NEW)
    else:
        circuit.append(cirq.ry(pi / 4).on(q1), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.measure(q1, key='1'), strategy=cirq.InsertStrategy.NEW)
    return circuit
