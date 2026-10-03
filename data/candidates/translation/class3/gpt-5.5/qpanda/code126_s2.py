# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    def _init_machine(machine):
        for name in ("init_qvm", "init", "initQVM"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    method()
                except TypeError:
                    pass
                break

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany", "qallocMany"):
            method = getattr(machine, name, None)
            if callable(method):
                qs = method(n)
                return qs
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(machine, name, None)
            if callable(method):
                return [method() for _ in range(n)]
        raise RuntimeError("Unable to allocate qubits with pyQPanda3.")

    def _new_prog():
        if hasattr(pq, "QProg"):
            return pq.QProg()
        if hasattr(pq, "create_empty_qprog"):
            return pq.create_empty_qprog()
        raise RuntimeError("Unable to create a quantum program with pyQPanda3.")

    def _as_matrix(value):
        arr = np.asarray(value, dtype=complex)
        if arr.ndim == 1 and arr.size == 4:
            arr = arr.reshape((2, 2))
        if arr.shape == (2, 2):
            return arr
        return None

    def _run_prog(machine, prog):
        last_error = None
        for name in ("directly_run", "run", "run_qprog", "execute"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return method(prog)
                except TypeError as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Unable to run a quantum program with pyQPanda3.")

    def _get_state(machine, run_result=None):
        for obj in ((run_result,) if run_result is not None else ()) + (machine,):
            for name in ("get_qstate", "get_state", "get_qstate_vector", "get_state_vector"):
                method = getattr(obj, name, None)
                if callable(method):
                    state = np.asarray(method(), dtype=complex).reshape(-1)
                    if state.size >= 2:
                        return state[:2]
        raise RuntimeError("Unable to obtain a state vector with pyQPanda3.")

    def _state_after_h(prep_one):
        machine = pq.CPUQVM()
        _init_machine(machine)
        q = _alloc_qubits(machine, 1)
        prog = _new_prog()
        if prep_one:
            prog << pq.X(q[0])
        prog << pq.H(q[0])
        result = _run_prog(machine, prog)
        return _get_state(machine, result)

    def _hadamard_matrix():
        machine = pq.CPUQVM()
        _init_machine(machine)
        q = _alloc_qubits(machine, 1)
        gate = pq.H(q[0])

        for name in ("get_matrix", "matrix", "to_matrix"):
            method = getattr(gate, name, None)
            if callable(method):
                try:
                    mat = _as_matrix(method())
                    if mat is not None:
                        return mat
                except Exception:
                    pass

        objects = [gate]
        try:
            circuit = pq.QCircuit()
            circuit << gate
            objects.append(circuit)
        except Exception:
            circuit = None
        try:
            prog = _new_prog()
            prog << (circuit if circuit is not None else gate)
            objects.append(prog)
        except Exception:
            pass

        for obj in objects:
            for name in ("get_matrix", "get_unitary", "matrix", "to_matrix"):
                func = getattr(pq, name, None)
                if callable(func):
                    try:
                        mat = _as_matrix(func(obj))
                        if mat is not None:
                            return mat
                    except Exception:
                        pass

        return np.column_stack((_state_after_h(False), _state_after_h(True)))

    op_a = _hadamard_matrix()
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))
