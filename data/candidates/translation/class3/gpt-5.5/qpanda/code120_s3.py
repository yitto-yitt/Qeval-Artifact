# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import cmath
import pyqpanda3.core as pq

def create_diagonal_circuit(diag):
    dim = len(diag)
    if dim < 1 or (dim & (dim - 1)) != 0:
        raise ValueError("Diagonal length must be a positive power of 2.")
    n = int(math.log2(dim))

    machine_cls = getattr(pq, "CPUQVM", None) or getattr(pq, "CPUSingleThreadQVM", None)
    machine = machine_cls()

    for init_name in ("init", "init_qvm"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
                break
            except Exception:
                pass

    if n:
        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
            if hasattr(machine, alloc_name):
                try:
                    qubits = list(getattr(machine, alloc_name)(n))
                    break
                except Exception:
                    pass
        if qubits is None:
            qubits = []
            for _ in range(n):
                allocated = False
                for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
                    if hasattr(machine, alloc_name):
                        try:
                            qubits.append(getattr(machine, alloc_name)())
                            allocated = True
                            break
                        except Exception:
                            pass
                if not allocated:
                    raise RuntimeError("Unable to allocate qubits in pyQPanda3.")
    else:
        qubits = []

    prog = pq.QProg()
    values = [complex(x) for x in diag]

    if n:
        matrix = [[0j for _ in range(dim)] for __ in range(dim)]
        for i, value in enumerate(values):
            matrix[i][i] = value
        flat_matrix = [matrix[i][j] for i in range(dim) for j in range(dim)]

        def append_obj(obj):
            try:
                prog << obj
                return True
            except Exception:
                try:
                    prog.insert(obj)
                    return True
                except Exception:
                    return False

        for builder_name in ("QOracle", "Oracle", "QUnitary", "Unitary"):
            builder = getattr(pq, builder_name, None)
            if builder is None:
                continue
            for mat in (matrix, flat_matrix):
                for args in ((qubits, mat), (mat, qubits), (qubits, mat, "Diagonal"), (mat, qubits, "Diagonal")):
                    try:
                        obj = builder(*args)
                        if append_obj(obj):
                            if not hasattr(create_diagonal_circuit, "_qpanda_machines"):
                                create_diagonal_circuit._qpanda_machines = []
                            create_diagonal_circuit._qpanda_machines.append(machine)
                            create_diagonal_circuit._last_qubits = qubits
                            return prog
                    except Exception:
                        pass

        for decomp_name in ("matrix_decompose", "MatrixDecompose"):
            decomp = getattr(pq, decomp_name, None)
            if decomp is None:
                continue
            for mat in (matrix, flat_matrix):
                try:
                    obj = decomp(qubits, mat)
                    if append_obj(obj):
                        if not hasattr(create_diagonal_circuit, "_qpanda_machines"):
                            create_diagonal_circuit._qpanda_machines = []
                        create_diagonal_circuit._qpanda_machines.append(machine)
                        create_diagonal_circuit._last_qubits = qubits
                        return prog
                except Exception:
                    pass

        rz_gate = getattr(pq, "RZ", None)
        cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
        if rz_gate is None or cnot_gate is None:
            raise RuntimeError("Required gates for diagonal decomposition are unavailable.")

        phases = [cmath.phase(v) for v in values]
        inv_dim = 1.0 / dim
        for mask in range(1, dim):
            beta = 0.0
            for x, phase in enumerate(phases):
                beta += phase if ((x & mask).bit_count() % 2 == 0) else -phase
            beta *= inv_dim
            angle = -2.0 * beta
            if abs(angle) < 1e-12:
                continue
            idx = [i for i in range(n) if (mask >> i) & 1]
            target = idx[-1]
            for control in idx[:-1]:
                prog << cnot_gate(qubits[control], qubits[target])
            prog << rz_gate(qubits[target], angle)
            for control in reversed(idx[:-1]):
                prog << cnot_gate(qubits[control], qubits[target])

    if not hasattr(create_diagonal_circuit, "_qpanda_machines"):
        create_diagonal_circuit._qpanda_machines = []
    create_diagonal_circuit._qpanda_machines.append(machine)
    create_diagonal_circuit._last_qubits = qubits
    return prog
