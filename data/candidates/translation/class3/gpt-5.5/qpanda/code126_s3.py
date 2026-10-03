# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    def _initialize_machine():
        machine = pq.CPUQVM()
        for name in ("init_qvm", "init"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                    break
                except TypeError:
                    continue
        return machine

    def _allocate_one_qubit(machine):
        for name in ("qAlloc_many", "qalloc_many"):
            method = getattr(machine, name, None)
            if method is not None:
                qubits = method(1)
                return qubits[0]
        for name in ("qAlloc", "qalloc"):
            method = getattr(machine, name, None)
            if method is not None:
                return method()
        raise RuntimeError("Unable to allocate qubit with pyqpanda3.core CPUQVM.")

    def _append_gate(prog, gate):
        try:
            new_prog = prog << gate
            return prog if new_prog is None else new_prog
        except Exception:
            result = prog.insert(gate)
            return prog if result is None else result

    def _state_to_vector(state):
        if isinstance(state, dict):
            vec = np.zeros(2, dtype=complex)
            for key, value in state.items():
                if isinstance(key, str):
                    idx = int(key, 2) if set(key) <= {"0", "1"} else int(key)
                else:
                    idx = int(key)
                if idx < 2:
                    vec[idx] = complex(value)
            return vec
        return np.asarray(state, dtype=complex).reshape(-1)[:2]

    def _run_h_on_basis(basis_index):
        machine = _initialize_machine()
        qubit = _allocate_one_qubit(machine)
        prog = pq.QProg()

        if basis_index == 1:
            prog = _append_gate(prog, pq.X(qubit))
        prog = _append_gate(prog, pq.H(qubit))

        executed = False
        run_result = None
        for name in ("directly_run", "run", "execute"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    run_result = method(prog)
                    executed = True
                    break
                except TypeError:
                    continue

        if not executed:
            for name in ("directly_run", "run"):
                method = getattr(pq, name, None)
                if method is not None:
                    try:
                        run_result = method(prog)
                        executed = True
                        break
                    except TypeError:
                        continue

        state = None
        for name in ("get_qstate", "getQState", "get_q_state", "get_state", "get_statevector", "getState"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    state = method()
                    break
                except TypeError:
                    continue

        if state is None:
            state = run_result

        vec = _state_to_vector(state)

        for name in ("finalize", "finalize_qvm"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                except TypeError:
                    pass
                break

        return vec

    op_a = np.column_stack((_run_h_on_basis(0), _run_h_on_basis(1)))
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))
