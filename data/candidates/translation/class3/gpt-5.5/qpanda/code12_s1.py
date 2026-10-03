# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *


def get_unitary():
    def _init_machine():
        machine = CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(machine, name, None)
            if callable(method):
                method()
                break
        return machine

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "qAlloc"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return method(n)
                except TypeError:
                    pass
        return [machine.qAlloc() for _ in range(n)]

    def _append(prog, gate):
        prog << gate
        return prog

    def _run_state(initial_bits):
        machine = _init_machine()
        q = _alloc_qubits(machine, 2)
        prog = QProg()
        if initial_bits[0]:
            _append(prog, X(q[0]))
        if initial_bits[1]:
            _append(prog, X(q[1]))
        _append(prog, H(q[0]))
        _append(prog, CNOT(q[0], q[1]))

        result = None
        for name in ("directly_run", "directlyRun", "run"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    result = method(prog)
                    break
                except TypeError:
                    continue

        for name in ("get_qstate", "get_qstate_vector", "get_state", "get_state_vector", "getQState"):
            method = getattr(machine, name, None)
            if callable(method):
                state = method()
                return np.asarray(state, dtype=complex)

        return np.asarray(result, dtype=complex)

    state_q0 = _run_state([1, 0])
    state_q1 = _run_state([0, 1])
    idx_q0 = int(np.argmax(np.abs(state_q0[:4])))
    idx_q1 = int(np.argmax(np.abs(state_q1[:4])))

    unitary = np.zeros((4, 4), dtype=complex)
    for col in range(4):
        state = _run_state([col & 1, (col >> 1) & 1])[:4]
        for py_index, amp in enumerate(state):
            row = (1 if (py_index & idx_q0) else 0) + (2 if (py_index & idx_q1) else 0)
            unitary[row, col] = amp

    return unitary
