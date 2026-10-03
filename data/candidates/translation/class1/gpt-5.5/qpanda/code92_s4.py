# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    try:
        machine.init_qvm()
    except Exception:
        pass

    alloc_many = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
        if hasattr(machine, name):
            alloc_many = getattr(machine, name)
            break
    if alloc_many is not None:
        qubits = alloc_many(2)
    else:
        alloc_one = getattr(machine, "qAlloc", getattr(machine, "qalloc"))
        qubits = [alloc_one(), alloc_one()]

    prog = QProg()

    def add_gate(gate):
        try:
            prog << gate
        except Exception:
            prog.insert(gate)

    add_gate(H(qubits[0]))
    cnot_ctor = globals().get("CNOT", globals().get("CX"))
    add_gate(cnot_ctor(qubits[0], qubits[1]))

    result = None
    if hasattr(machine, "prob_run_dict"):
        method = getattr(machine, "prob_run_dict")
        for args in ((prog, qubits, -1), (prog, qubits), (prog, list(qubits), -1), (prog, list(qubits))):
            try:
                result = method(*args)
                break
            except Exception:
                pass

    if result is None:
        ran = False
        for name in ("directly_run", "run"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)(prog)
                    ran = True
                    break
                except Exception:
                    pass

        if hasattr(machine, "get_prob_dict"):
            method = getattr(machine, "get_prob_dict")
            for args in ((qubits, -1), (qubits,), (prog, qubits, -1), (prog, qubits), ()):
                try:
                    result = method(*args)
                    break
                except Exception:
                    pass

        if result is None:
            if not ran:
                for name in ("directly_run", "run"):
                    if hasattr(machine, name):
                        try:
                            getattr(machine, name)(prog)
                            break
                        except Exception:
                            pass
            state = None
            for name in ("get_qstate", "get_qstate_vector", "get_state_vector"):
                if hasattr(machine, name):
                    try:
                        state = getattr(machine, name)()
                        break
                    except Exception:
                        pass
            result = {}
            if isinstance(state, dict):
                for k, amp in state.items():
                    key = k if isinstance(k, str) else format(int(k), "02b")
                    result[key.zfill(2)] = abs(amp) ** 2
            else:
                for i, amp in enumerate(state):
                    result[format(i, "02b")] = abs(amp) ** 2

    probabilities_dict = {}
    for k, v in result.items():
        key = k if isinstance(k, str) else format(int(k), "02b")
        key = key.replace(" ", "").zfill(2)
        try:
            val = float(v.real)
        except Exception:
            val = float(v)
        if abs(val) > 1e-12:
            probabilities_dict[key] = round(val, 12)

    return dict(sorted(probabilities_dict.items()))
