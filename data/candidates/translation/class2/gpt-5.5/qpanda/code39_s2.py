# EVAL_META: task_id=39, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def create_uniform_superposition(n):
    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(n)
    else:
        qubits = qvm.qalloc_many(n)

    prog = pq.QProg()
    for i in range(n):
        prog << pq.H(qubits[i])

    run_result = None
    for run_call in (
        lambda: qvm.directly_run(prog),
        lambda: qvm.run(prog),
        lambda: qvm.run(prog, 1),
    ):
        try:
            run_result = run_call()
            break
        except Exception:
            pass

    for state_name in ("get_qstate", "get_qstate_vector", "get_statevector", "get_state"):
        if hasattr(qvm, state_name):
            try:
                return getattr(qvm, state_name)()
            except Exception:
                pass

    if run_result is not None and not isinstance(run_result, (dict, int, float, str)):
        return run_result

    for prob_call in (
        lambda: qvm.prob_run_list(prog, qubits, -1),
        lambda: qvm.prob_run_list(prog, qubits),
    ):
        try:
            probs = prob_call()
            return np.sqrt(np.asarray(probs, dtype=float)).astype(complex)
        except Exception:
            pass

    probs = qvm.prob_run_dict(prog, qubits, -1)
    state = np.zeros(2 ** n, dtype=complex)
    for key, value in probs.items():
        idx = int(key, 2) if isinstance(key, str) else int(key)
        state[idx] = np.sqrt(float(value))
    return state
