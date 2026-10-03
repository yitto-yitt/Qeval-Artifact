# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, H, S, X, Y, Z, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def _circuit_unitary(circuit, num_qubits):
    prog = QProg()
    prog << circuit
    mat = np.array(machine.get_unitary(prog)).reshape(2 ** num_qubits, 2 ** num_qubits)
    return mat


def _equiv(u1, u2, rtol=0.4, atol=0.4):
    dim = u1.shape[0]
    inner = np.vdot(u1.reshape(-1), u2.reshape(-1))
    if abs(inner) < 1e-12:
        return False
    phase = inner / abs(inner)
    return np.allclose(u1 * np.conjugate(phase), u2, rtol=rtol, atol=atol)


def _random_clifford_circuit(num_qubits, qbs):
    circ = QCircuit()
    single_gates = [H, S, X, Y, Z]
    depth = num_qubits * 2 + 2
    for _ in range(depth):
        for q in range(num_qubits):
            g = single_gates[np.random.randint(len(single_gates))]
            circ << g(qbs[q])
        if num_qubits >= 2:
            for q in range(num_qubits - 1):
                if np.random.randint(2) == 0:
                    circ << CNOT(qbs[q], qbs[q + 1])
    return circ


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits if hasattr(circuit, "num_qubits") else len(circuit)
    qbs = [qubits[i] for i in range(num_qubits)]

    op_or = _circuit_unitary(circuit, num_qubits)

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits, qbs)
        op_qc = _circuit_unitary(qc, num_qubits)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)

    return qc_list


machine.finalize()
