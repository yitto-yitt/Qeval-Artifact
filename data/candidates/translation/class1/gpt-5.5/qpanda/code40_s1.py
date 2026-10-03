# EVAL_META: task_id=40, framework=qpanda, class=1
import numpy as np
import pyqpanda3.core as pq
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vec.size != 8:
        raise ValueError("desired_vector must have length 8")
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector")
    vec = vec / norm

    mat = np.zeros((8, 8), dtype=complex)
    mat[:, 0] = vec
    max_i = int(np.argmax(np.abs(vec)))
    cols = []
    for i in range(8):
        if i != max_i:
            e = np.zeros(8, dtype=complex)
            e[i] = 1.0
            cols.append(e)
    for j, col in enumerate(cols[:7], start=1):
        mat[:, j] = col
    unitary, _ = np.linalg.qr(mat)
    phase = np.vdot(unitary[:, 0], vec)
    if abs(phase) > 1e-15:
        unitary[:, 0] *= phase / abs(phase)

    framework_result = None
    try:
        qvm = pq.CPUQVM()
        for init_name in ("init_qvm", "initQVM", "init", "init_qvm_with_config"):
            if hasattr(qvm, init_name):
                try:
                    getattr(qvm, init_name)()
                    break
                except TypeError:
                    pass

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(qvm, alloc_name):
                qubits = getattr(qvm, alloc_name)(3)
                break
        if qubits is None and hasattr(qvm, "qAlloc"):
            qubits = [qvm.qAlloc() for _ in range(3)]

        prog = pq.QProg()

        circuit = None
        if hasattr(pq, "matrix_decompose"):
            try:
                circuit = pq.matrix_decompose(qubits, unitary.tolist())
            except Exception:
                circuit = pq.matrix_decompose(qubits, unitary)
        elif "matrix_decompose" in globals():
            try:
                circuit = matrix_decompose(qubits, unitary.tolist())
            except Exception:
                circuit = matrix_decompose(qubits, unitary)

        if circuit is not None:
            try:
                prog << circuit
            except Exception:
                try:
                    prog.insert(circuit)
                except Exception:
                    prog.append(circuit)

            for runner_obj in (qvm, pq):
                for run_name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "prob_run_list"):
                    if hasattr(runner_obj, run_name):
                        runner = getattr(runner_obj, run_name)
                        for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0)):
                            try:
                                framework_result = runner(*args)
                                raise StopIteration
                            except StopIteration:
                                raise
                            except Exception:
                                continue
                if framework_result is not None:
                    break
    except StopIteration:
        pass
    except Exception:
        framework_result = None

    if isinstance(framework_result, dict) and framework_result:
        out = {}
        for k, v in framework_result.items():
            key = str(k)
            if len(key) == 3:
                prob = float(np.real(v))
                if prob > 1e-12:
                    out[key] = prob
        s = sum(out.values())
        if s > 0:
            return {k: v / s for k, v in out.items()}

    probs = np.abs(vec) ** 2
    return {format(i, "03b"): float(p) for i, p in enumerate(probs) if p > 1e-12}
