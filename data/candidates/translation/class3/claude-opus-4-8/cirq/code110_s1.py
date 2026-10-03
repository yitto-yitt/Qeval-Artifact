# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def _operator_equiv(u1, u2, rtol=0.4, atol=0.4):
    d = u1.shape[0]
    val = np.vdot(u1.flatten(), u2.flatten()) / d
    if abs(val) < 1e-12:
        return False
    phase = val / abs(val)
    return np.allclose(u1, phase * u2, rtol=rtol, atol=atol)


def _random_clifford_circuit(qubits):
    n = len(qubits)
    circuit = cirq.Circuit()
    num_ops = np.random.randint(1, 6 * n + 1)
    for _ in range(num_ops):
        choice = np.random.randint(0, 4 if n > 1 else 3)
        if choice == 0:
            q = qubits[np.random.randint(n)]
            circuit.append(cirq.H(q))
        elif choice == 1:
            q = qubits[np.random.randint(n)]
            circuit.append(cirq.S(q))
        elif choice == 2:
            q = qubits[np.random.randint(n)]
            circuit.append(cirq.X(q))
        else:
            i = np.random.randint(n)
            j = np.random.randint(n)
            while j == i:
                j = np.random.randint(n)
            circuit.append(cirq.CNOT(qubits[i], qubits[j]))
    return circuit


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    if not qubits:
        qubits = [cirq.LineQubit(0)]
    num_qubits = len(qubits)

    ref_circuit = cirq.Circuit()
    ref_circuit.append(circuit.all_operations())
    op_or = cirq.unitary(cirq.Circuit(
        [cirq.I(q) for q in qubits] + list(ref_circuit.all_operations())
    ))

    line_qubits = [cirq.LineQubit(i) for i in range(num_qubits)]

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(line_qubits)
        full = cirq.Circuit([cirq.I(q) for q in line_qubits] + list(qc.all_operations()))
        op_qc = cirq.unitary(full)
        if op_qc.shape == op_or.shape and _operator_equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
