# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
import numpy as np


def chsh_circuit(alice, bob):
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()

    # Bell state preparation
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))

    # Alice's measurement basis rotation
    if alice == 0:
        circuit.append(cirq.ry(0)(qubits[0]))
    else:
        circuit.append(cirq.ry(-np.pi / 2)(qubits[0]))

    # Bob's measurement basis rotation
    if bob == 0:
        circuit.append(cirq.ry(-np.pi / 4)(qubits[1]))
    else:
        circuit.append(cirq.ry(np.pi / 4)(qubits[1]))

    # Measurements
    circuit.append(cirq.measure(*qubits))

    return circuit
