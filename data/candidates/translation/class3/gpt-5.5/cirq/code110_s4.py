# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(circuit.all_qubits()))
    rng = np.random.default_rng()
    qc_list = []

    for _ in range(max(0, n)):
        qc = cirq.Circuit(circuit)

        if qubits:
            num_pairs = int(rng.integers(1, 4 * len(qubits) + 2))
            for _ in range(num_pairs):
                if len(qubits) >= 2 and rng.random() < 0.4:
                    q0, q1 = rng.choice(qubits, size=2, replace=False)
                    gate_choice = int(rng.integers(0, 3))
                    if gate_choice == 0:
                        op = cirq.CNOT(q0, q1)
                    elif gate_choice == 1:
                        op = cirq.CZ(q0, q1)
                    else:
                        op = cirq.SWAP(q0, q1)
                else:
                    q = rng.choice(qubits)
                    gate_choice = int(rng.integers(0, 6))
                    if gate_choice == 0:
                        op = cirq.X(q)
                    elif gate_choice == 1:
                        op = cirq.Y(q)
                    elif gate_choice == 2:
                        op = cirq.Z(q)
                    elif gate_choice == 3:
                        op = cirq.H(q)
                    elif gate_choice == 4:
                        op = cirq.S(q)
                    else:
                        op = cirq.S(q) ** -1

                if rng.random() < 0.5:
                    qc.append([op, op ** -1])
                else:
                    qc = cirq.Circuit([op, op ** -1]) + qc

        qc_list.append(qc)

    return qc_list
