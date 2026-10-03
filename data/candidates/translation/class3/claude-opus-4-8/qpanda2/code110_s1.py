# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, H, S, X, Y, Z, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)

_SINGLE = [
    lambda q: H(q),
    lambda q: S(q),
    lambda q: X(q),
    lambda q: Y(q),
    lambda q: Z(q),
]


def _infer_num_qubits(circuit):
    try:
        return circuit.get_max_qubit_addr() + 1
    except Exception:
        pass
    try:
        return circuit.get_qubit_num()
    except Exception:
        return 1


def _prep_basis(prog, qs, col, num_qubits):
    for i in range(num_qubits):
        if (col >> i) & 1:
            prog << X(qs[i])


def _unitary_from_ops(ops, num_qubits):
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=complex)
    qs = qubits[:num_qubits]
    for col in range(dim):
        prog = QProg()
        _prep_basis(prog, qs, col, num_qubits)
        for op in ops:
            if op[0] == 'cx':
                prog << CNOT(qs[op[1]], qs[op[2]])
            else:
                prog << _SINGLE[op[2]](qs[op[1]])
        machine.directly_run(prog)
        state = np.array(machine.get_qstate(), dtype=complex)
        U[:, col] = state
    return U


def _unitary_from_circuit(circuit, num_qubits):
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=complex)
    qs = qubits[:num_qubits]
    for col in range(dim):
        prog = QProg()
        _prep_basis(prog, qs, col, num_qubits)
        prog << circuit
        machine.directly_run(prog)
        state = np.array(machine.get_qstate(), dtype=complex)
        U[:, col] = state
    return U


def _random_clifford_ops(num_qubits, rng):
    ops = []
    depth = 4 * num_qubits + 4
    for _ in range(depth):
        if num_qubits > 1 and rng.random() < 0.4:
            a, b = rng.choice(num_qubits, size=2, replace=False)
            ops.append(('cx', int(a), int(b)))
        else:
            q = int(rng.integers(0, num_qubits))
            g = int(rng.integers(0, len(_SINGLE)))
            ops.append(('s', q, g))
    return ops


def _equiv(u1, u2, rtol=0.4, atol=0.4):
    dim = u1.shape[0]
    prod = u1.conj().T @ u2
    diag = np.diag(prod)
    if np.max(np.abs(diag)) < 1e-9:
        return False
    ref = diag[int(np.argmax(np.abs(diag)))]
    ref = ref / abs(ref)
    scaled = u2 / ref
    diff = np.abs(scaled - u1)
    tol = atol + rtol * np.abs(u1)
    return bool(np.all(diff <= tol))


def equivalent_clifford_circuit(circuit, n):
    num_qubits = _infer_num_qubits(circuit)
    ref_U = _unitary_from_circuit(circuit, num_qubits)
    rng = np.random.default_rng()
    qs = qubits[:num_qubits]
    qc_list = []
    counter = 0
    while counter < n:
        ops = _random_clifford_ops(num_qubits, rng)
        cand_U = _unitary_from_ops(ops, num_qubits)
        if _equiv(cand_U, ref_U, rtol=0.4, atol=0.4):
            qc = QCircuit()
            for op in ops:
                if op[0] == 'cx':
                    qc << CNOT(qs[op[1]], qs[op[2]])
                else:
                    qc << _SINGLE[op[2]](qs[op[1]])
            qc_list.append(qc)
            counter += 1
    return qc_list


machine.finalize()
