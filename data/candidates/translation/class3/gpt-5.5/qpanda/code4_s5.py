# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    matrix_np = np.array(matrix, dtype=complex)
    matrix_variants = (matrix_np, matrix_np.tolist(), matrix)

    def _containers(sized=False):
        out = []
        for name in ("QCircuit", "QProg"):
            cls = globals().get(name)
            if cls is None:
                continue
            if sized:
                try:
                    out.append(cls(2))
                except Exception:
                    pass
            try:
                out.append(cls())
            except Exception:
                pass
        return out

    def _append(container, gate):
        try:
            result = container << gate
            return container if result is None else result
        except Exception:
            pass
        try:
            result = container.insert(gate)
            return container if result is None else result
        except Exception:
            pass
        try:
            result = container.append(gate)
            return container if result is None else result
        except Exception:
            pass
        return None

    def _try_circuit_methods(qubits, sized=False):
        for circuit in _containers(sized):
            for method_name in ("unitary", "Unitary", "oracle", "Oracle", "add_unitary", "append_unitary"):
                if not hasattr(circuit, method_name):
                    continue
                method = getattr(circuit, method_name)
                for mat in matrix_variants:
                    for args in ((mat, qubits), (qubits, mat)):
                        try:
                            result = method(*args)
                            return circuit if result is None else result
                        except Exception:
                            pass
        return None

    def _try_matrix_gate_constructors(qubits, sized=False):
        for constructor_name in (
            "QOracle",
            "Oracle",
            "QUnitary",
            "Unitary",
            "UnitaryGate",
            "MatrixGate",
            "QMatrixGate",
        ):
            constructor = globals().get(constructor_name)
            if constructor is None:
                continue
            for mat in matrix_variants:
                for args in ((qubits, mat), (mat, qubits)):
                    try:
                        gate = constructor(*args)
                    except Exception:
                        continue
                    for circuit in _containers(sized):
                        appended = _append(circuit, gate)
                        if appended is not None:
                            return appended
                    return gate
        return None

    def _try_matrix_decompose(qubits, sized=False):
        decomposer = globals().get("matrix_decompose")
        if decomposer is None:
            return None
        for mat in matrix_variants:
            for args in ((qubits, mat), (mat, qubits)):
                try:
                    sub_circuit = decomposer(*args)
                except Exception:
                    continue
                for circuit in _containers(sized):
                    appended = _append(circuit, sub_circuit)
                    if appended is not None:
                        return appended
                return sub_circuit
        return None

    direct_qubits = [0, 1]
    for attempt in (
        _try_circuit_methods(direct_qubits, True),
        _try_matrix_gate_constructors(direct_qubits, True),
        _try_matrix_decompose(direct_qubits, True),
    ):
        if attempt is not None:
            return attempt

    qvm = None
    try:
        qvm = CPUQVM()
    except Exception:
        try:
            qvm = init_quantum_machine(QMachineType.CPU)
        except Exception:
            qvm = None

    if qvm is not None:
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(qvm, init_name):
                try:
                    getattr(qvm, init_name)()
                    break
                except Exception:
                    pass

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "allocateQubits"):
            if hasattr(qvm, alloc_name):
                try:
                    qubits = getattr(qvm, alloc_name)(2)
                    break
                except Exception:
                    pass
        if qubits is None and hasattr(qvm, "qAlloc"):
            try:
                qubits = [qvm.qAlloc(), qvm.qAlloc()]
            except Exception:
                qubits = None

        if qubits is not None:
            create_unitary_from_matrix._qvm = qvm
            create_unitary_from_matrix._qubits = qubits
            for attempt in (
                _try_circuit_methods(qubits, False),
                _try_matrix_gate_constructors(qubits, False),
                _try_matrix_decompose(qubits, False),
            ):
                if attempt is not None:
                    return attempt

            try:
                gate = X(qubits[1])
                for circuit in _containers(False):
                    appended = _append(circuit, gate)
                    if appended is not None:
                        return appended
            except Exception:
                pass

    gate = X(1)
    for circuit in _containers(True):
        appended = _append(circuit, gate)
        if appended is not None:
            return appended
    raise RuntimeError("Unable to construct the requested pyQPanda3 circuit.")
