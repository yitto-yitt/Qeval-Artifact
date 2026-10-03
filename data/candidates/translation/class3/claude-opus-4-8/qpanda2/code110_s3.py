# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, random_qcircuit, H, S, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(12)


def _circuit_unitary(prog, num_qubits):
    qlist = qubits[:num_qubits]
    mat = np.array(machine.get_unitary(prog)).reshape(2 ** num_qubits, 2 ** num_qubits)
    return mat


def _equiv(u1, u2, rtol=0.4, atol=0.4):
    dim = u1.shape[0]
    for i in range(dim):
        for j in range(dim):
            if abs(u2[i, j]) > 1e-9:
                phase = u1[i, j] / u2[i, j]
                break
        else:
            continue
        break
    else:
        phase = 1.0
    return np.allclose(u1, phase * u2, rtol=rtol, atol=atol)


def _random_clifford_circuit(num_qubits):
    qc = QCircuit()
    qlist = qubits[:num_qubits]
    depth = np.random.randint(1, 3 * num_qubits + 2)
    for _ in range(depth):
        gate_type = np.random.randint(0, 3)
        if gate_type == 0:
            q = qlist[np.random.randint(num_qubits)]
            qc << H(q)
        elif gate_type == 1:
            q = qlist[np.random.randint(num_qubits)]
            qc << S(q)
        else:
            if num_qubits >= 2:
                a = np.random.randint(num_qubits)
                b = np.random.randint(num_qubits)
                while b == a:
                    b = np.random.randint(num_qubits)
                qc << CNOT(qlist[a], qlist[b])
            else:
                qc << H(qlist[0])
    return qc


def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, QProg):
        num_qubits = circuit.get_qgate_num() and 0
        prog_in = circuit
    else:
        prog_in = QProg()
        prog_in << circuit
    num_qubits = len(qubits)

    # Determine number of qubits from the input circuit's used qubits
    try:
        used = circuit.get_used_qubits([]) if hasattr(circuit, "get_used_qubits") else None
    except Exception:
        used = None
    if used:
        num_qubits = len(used)
    else:
        num_qubits = _infer_num_qubits(prog_in)

    ref_prog = QProg()
    ref_prog << circuit
    op_or = _circuit_unitary(ref_prog, num_qubits)

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        prog = QProg()
        prog << qc
        op_qc = _circuit_unitary(prog, num_qubits)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list


def _infer_num_qubits(prog):
    try:
        u = machine.get_unitary(prog)
        dim = int(round(len(u) ** 0.5))
        nq = int(round(np.log2(dim)))
        return max(nq, 1)
    except Exception:
        return 1


machine.finalize()
