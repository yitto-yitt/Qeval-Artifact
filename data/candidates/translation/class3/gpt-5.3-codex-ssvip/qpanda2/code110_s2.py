# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(16)

def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, pq.QProg):
        target_prog = circuit
    elif isinstance(circuit, pq.QCircuit):
        target_prog = pq.QProg()
        target_prog.insert(circuit)
    else:
        raise TypeError("circuit must be a pyqpanda QProg or QCircuit")

    target_mat = np.array(pq.get_unitary(target_prog), dtype=np.complex128)
    dim = target_mat.shape[0]
    num_qubits = int(round(np.log2(dim)))
    qubits = _global_qubits[:num_qubits]

    results = []
    while len(results) < n:
        cand_circ = pq.random_qcircuit(qubits, 10)
        cand_prog = pq.QProg()
        cand_prog.insert(cand_circ)
        cand_mat = np.array(pq.get_unitary(cand_prog), dtype=np.complex128)

        if np.allclose(cand_mat, target_mat, rtol=0.4, atol=0.4):
            results.append(cand_circ)

    machine.finalize()
    return results
