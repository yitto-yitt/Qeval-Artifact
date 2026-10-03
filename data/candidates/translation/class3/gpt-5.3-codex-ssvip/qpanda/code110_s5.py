# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np
import random

def equivalent_clifford_circuit(circuit, n):
    def _extract_qubit_count(circ):
        if hasattr(circ, "qubit_num"):
            qn = circ.qubit_num
            return qn() if callable(qn) else int(qn)
        if hasattr(circ, "get_qubit_num"):
            return int(circ.get_qubit_num())
        if hasattr(circ, "n_qubits"):
            qn = circ.n_qubits
            return qn() if callable(qn) else int(qn)
        if hasattr(circ, "num_qubits"):
            qn = circ.num_qubits
            return qn() if callable(qn) else int(qn)
        raise ValueError("Unable to determine qubit count from input circuit.")

    def _unitary_of_prog(prog, num_qubits):
        m = get_matrix(prog)
        arr = np.array(m, dtype=complex)
        dim = 1 << num_qubits
        arr = arr.reshape((dim, dim))
        return arr

    def _random_clifford_like_prog(qubits):
        prog = QProg()
        depth = random.randint(1, 6)
        for _ in range(depth):
            for q in qubits:
                r = random.randint(0, 2)
                if r == 0:
                    prog << H(q)
                elif r == 1:
                    prog << S(q)
                else:
                    prog << X(q)
            if len(qubits) > 1:
                pairs = list(range(len(qubits) - 1))
                random.shuffle(pairs)
                for i in pairs:
                    if random.random() < 0.5:
                        prog << CNOT(qubits[i], qubits[i + 1])
        return prog

    def _equiv(u, v, rtol=0.4, atol=0.4):
        idx = np.unravel_index(np.argmax(np.abs(v)), v.shape)
        denom = v[idx]
        if abs(denom) < 1e-12:
            return np.allclose(u, v, rtol=rtol, atol=atol)
        phase = u[idx] / denom
        return np.allclose(u, phase * v, rtol=rtol, atol=atol)

    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        num_qubits = _extract_qubit_count(circuit)
        q = qvm.qAlloc_many(num_qubits)

        if isinstance(circuit, QProg):
            target_prog = circuit
        else:
            target_prog = QProg() << circuit

        op_or = _unitary_of_prog(target_prog, num_qubits)

        qc_list = []
        counter = 0
        while counter < n:
            qc = _random_clifford_like_prog(q)
            op_qc = _unitary_of_prog(qc, num_qubits)
            if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
                qc_list.append(qc)
                counter += 1
        return qc_list
    finally:
        qvm.finalize()
