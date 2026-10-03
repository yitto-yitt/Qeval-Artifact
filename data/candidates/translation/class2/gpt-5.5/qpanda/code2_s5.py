# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_bell_statevector():
    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
    else:
        qvm = pq.init_quantum_machine(pq.QMachineType.CPU)

    for name in ("init_qvm", "initQVM", "init", "initialize"):
        method = getattr(qvm, name, None)
        if method is not None:
            try:
                method()
                break
            except TypeError:
                pass

    qubits = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits"):
        method = getattr(qvm, name, None)
        if method is not None:
            try:
                qubits = method(2)
                break
            except TypeError:
                pass

    if qubits is None:
        raise RuntimeError("Unable to allocate qubits with pyQPanda3 CPUQVM.")

    prog = pq.QProg()
    cnot = getattr(pq, "CNOT", getattr(pq, "CX", None))
    prog << pq.H(qubits[0]) << cnot(qubits[0], qubits[1])

    run_result = None
    ran = False
    for name in ("directly_run", "direct_run", "run_qprog", "run"):
        method = getattr(qvm, name, None)
        if method is not None:
            try:
                run_result = method(prog)
                ran = True
                break
            except TypeError:
                pass

    if not ran and hasattr(pq, "directly_run"):
        run_result = pq.directly_run(prog)
        ran = True

    if not ran:
        raise RuntimeError("Unable to execute quantum program with pyQPanda3 CPUQVM.")

    for owner in (qvm, pq):
        for name in (
            "get_qstate",
            "get_qstate_vector",
            "get_state_vector",
            "get_statevector",
            "get_state",
            "statevector",
        ):
            method = getattr(owner, name, None)
            if method is not None:
                for args in ((), (qubits,), (qvm,), (qvm, qubits)):
                    try:
                        return method(*args)
                    except TypeError:
                        pass

    if run_result is not None:
        return run_result

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 CPUQVM.")
