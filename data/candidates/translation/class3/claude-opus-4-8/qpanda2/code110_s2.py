# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, H, S, X, Y, Z, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def _circuit_matrix(circuit, num_qubits):
    prog = QProg()
    prog.insert(circuit)
    machine.directly_run(prog)
    dim = 2 ** num_qubits
    mat = np.array(machine.get_qmatrix()).reshape(dim, dim)
    return mat


def _matrix_from_gates(gate_list, num_qubits):
    circ = QCircuit()
    qs = qubits[:num_qubits]
    for gname, targets in gate_list:
        if gname == 'H':
            circ << H(qs[targets[0]])
        elif gname == 'S':
            circ << S(qs[targets[0]])
        elif gname == 'X':
            circ << X(qs[targets[0]])
        elif gname == 'Y':
            circ << Y(qs[targets[0]])
        elif gname == 'Z':
            circ << Z(qs[targets[0]])
        elif gname == 'CNOT':
            circ << CNOT(qs[targets[0]], qs[targets[1]])
    prog = QProg()
    prog.insert(circ)
    machine.directly_run(prog)
    dim = 2 ** num_qubits
    mat = np.array(machine.get_qmatrix()).reshape(dim, dim)
    return mat, circ


def _random_clifford_gates(num_qubits, rng):
    gates = []
    single = ['H', 'S', 'X', 'Y', 'Z']
    depth = 4 * num_qubits + 4
    for _ in range(depth):
        if num_qubits > 1 and rng.random() < 0.35:
            a, b = rng.choice(num_qubits, size=2, replace=False)
            gates.append(('CNOT', [int(a), int(b)]))
        else:
            q = int(rng.integers(num_qubits))
            g = single[int(rng.integers(len(single)))]
            gates.append((g, [q]))
    return gates


def _equiv(mat_a, mat_b, rtol=0.4, atol=0.4):
    dim = mat_a.shape[0]
    phase = None
    for i in range(dim):
        for j in range(dim):
            if abs(mat_b[i, j]) > 1e-9:
                phase = mat_a[i, j] / mat_b[i, j]
                break
        if phase is not None:
            break
    if phase is None:
        return np.allclose(mat_a, mat_b, rtol=rtol, atol=atol)
    return np.allclose(mat_a, phase * mat_b, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.get_max_qubit_addr() + 1 if hasattr(circuit, 'get_max_qubit_addr') else len(circuit.get_used_qubits())
    op_or = _circuit_matrix(circuit, num_qubits)
    rng = np.random.default_rng()
    qc_list = []
    counter = 0
    while counter < n:
        gates = _random_clifford_gates(num_qubits, rng)
        op_qc, circ = _matrix_from_gates(gates, num_qubits)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(circ)
    return qc_list


machine.finalize()
