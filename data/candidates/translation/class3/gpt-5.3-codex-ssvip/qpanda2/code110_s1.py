# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(32)


def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, pq.QProg):
        target_prog = circuit
    elif isinstance(circuit, pq.QCircuit):
        target_prog = pq.QProg() << circuit
    else:
        raise TypeError("circuit must be a pyqpanda QProg or QCircuit")

    target_u = np.array(pq.get_unitary(target_prog), dtype=complex)
    dim = target_u.shape[0]
    num_qubits = int(round(np.log2(dim)))

    if num_qubits > len(_global_qubits):
        raise ValueError("Not enough globally allocated qubits")

    q = _global_qubits[:num_qubits]
    out = []

    while len(out) < n:
        cand_circ = pq.random_qcircuit(q)
        cand_prog = pq.QProg() << cand_circ
        cand_u = np.array(pq.get_unitary(cand_prog), dtype=complex)

        if cand_u.shape != target_u.shape:
            continue

        if np.allclose(cand_u, target_u, rtol=0.4, atol=0.4):
            out.append(cand_circ)

    machine.finalize()
    return out
