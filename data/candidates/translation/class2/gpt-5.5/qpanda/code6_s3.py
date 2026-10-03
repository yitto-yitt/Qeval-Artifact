# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep(num_qubits):
    num_qubits = int(num_qubits)

    def _new_program():
        for cls_name in ("QProg", "QCircuit"):
            cls = getattr(pq, cls_name, None)
            if cls is None:
                continue
            try:
                return cls()
            except Exception:
                try:
                    return cls(num_qubits)
                except Exception:
                    pass
        raise RuntimeError("No pyQPanda3 program/circuit container is available.")

    def _append(container, operation):
        try:
            result = container << operation
            return container if result is None else result
        except Exception:
            if hasattr(container, "insert"):
                result = container.insert(operation)
                return container if result is None else result
            if hasattr(container, "append"):
                result = container.append(operation)
                return container if result is None else result
            raise

    def _identity_gate(qubit):
        for name in ("I", "ID", "Id", "Identity"):
            gate = getattr(pq, name, None)
            if gate is not None:
                try:
                    return gate(qubit)
                except Exception:
                    pass
        return None

    if num_qubits <= 0:
        return _new_program()

    try:
        prog = _new_program()
        for i in range(num_qubits):
            ident = _identity_gate(i)
            if ident is not None:
                prog = _append(prog, ident)
        prog = _append(prog, pq.X(0))
        return prog
    except Exception:
        pass

    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        init = getattr(machine, init_name, None)
        if init is not None:
            try:
                init()
                break
            except Exception:
                pass

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        alloc = getattr(machine, alloc_name, None)
        if alloc is not None:
            try:
                qubits = alloc(num_qubits)
                break
            except Exception:
                pass

    if qubits is None:
        alloc_one = None
        for alloc_name in ("qAlloc", "qalloc", "qAllocOne", "qallocOne"):
            alloc_one = getattr(machine, alloc_name, None)
            if alloc_one is not None:
                break
        qubits = [alloc_one() for _ in range(num_qubits)]

    if not hasattr(create_state_prep, "_machines"):
        create_state_prep._machines = []
    create_state_prep._machines.append((machine, qubits))

    prog = _new_program()
    for i in range(num_qubits):
        ident = _identity_gate(qubits[i])
        if ident is not None:
            prog = _append(prog, ident)
    prog = _append(prog, pq.X(qubits[0]))
    return prog
