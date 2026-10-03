# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QGate, H, S, X, Y, Z, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def _random_clifford_circuit(num_qubits):
    qc = QCircuit()
    depth = 4 * num_qubits + 4
    single_gates = ['H', 'S', 'X', 'Y', 'Z']
    for _ in range(depth):
        choice = np.random.randint(0, 2)
        if choice == 0 or num_qubits < 2:
            q = np.random.randint(0, num_qubits)
            g = single_gates[np.random.randint(0, len(single_gates))]
            if g == 'H':
                qc << H(qubits[q])
            elif g == 'S':
                qc << S(qubits[q])
            elif g == 'X':
                qc << X(qubits[q])
            elif g == 'Y':
                qc << Y(qubits[q])
            elif g == 'Z':
                qc << Z(qubits[q])
        else:
            c = np.random.randint(0, num_qubits)
            t = np.random.randint(0, num_qubits)
            while t == c:
                t = np.random.randint(0, num_qubits)
            qc << CNOT(qubits[c], qubits[t])
    return qc


def _unitary_of_circuit(qc, num_qubits):
    prog = QCircuit()
    prog << qc
    machine.directly_run(prog << QCircuit())
    mat = np.array(machine.get_unitary(prog)).reshape(
        (2 ** num_qubits, 2 ** num_qubits))
    return mat


def _equiv(u1, u2, rtol=0.4, atol=0.4):
    dim = u1.shape[0]
    # find a phase to align
    prod = u1.conj().T @ u2
    # if u1^dag u2 is close to phase*I
    diag = np.diagonal(prod)
    idx = np.argmax(np.abs(diag))
    phase = diag[idx]
    if abs(phase) < 1e-12:
        return False
    phase = phase / abs(phase)
    aligned = u2 / phase
    return np.allclose(u1, aligned, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits if hasattr(circuit, 'num_qubits') else circuit
    # Build reference unitary
    ref_prog = QCircuit()
    ref_prog << circuit
    machine.directly_run(ref_prog << QCircuit())
    op_or = np.array(machine.get_unitary(ref_prog)).reshape(
        (2 ** num_qubits, 2 ** num_qubits))

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        op_qc = _unitary_of_circuit(qc, num_qubits)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
