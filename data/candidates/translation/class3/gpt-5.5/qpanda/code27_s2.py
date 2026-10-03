# EVAL_META: task_id=27, framework=qpanda, class=3
import pyqpanda3.core as pq


def apply_op_back():
    machine = None

    machine_cls = getattr(pq, "CPUQVM", None)
    if machine_cls is not None:
        machine = machine_cls()
    elif hasattr(pq, "init_quantum_machine"):
        qmachine_type = getattr(pq, "QMachineType", None)
        if qmachine_type is not None:
            machine_type = getattr(qmachine_type, "CPU", None)
            if machine_type is None:
                machine_type = getattr(qmachine_type, "CPU_SINGLE_THREAD", None)
            machine = pq.init_quantum_machine(machine_type)

    if machine is None:
        raise RuntimeError("No available pyQPanda3 quantum machine backend found.")

    for init_name in ("init_qvm", "initQVM", "init"):
        init_fn = getattr(machine, init_name, None)
        if init_fn is not None:
            try:
                init_fn()
                break
            except TypeError:
                pass

    q = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        alloc_fn = getattr(machine, alloc_name, None)
        if alloc_fn is not None:
            q = alloc_fn(3)
            break

    if q is None:
        for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
            alloc_fn = getattr(machine, alloc_name, None)
            if alloc_fn is not None:
                q = [alloc_fn() for _ in range(3)]
                break

    if q is None:
        raise RuntimeError("No available pyQPanda3 qubit allocator found.")

    c = None
    for calloc_name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
        calloc_fn = getattr(machine, calloc_name, None)
        if calloc_fn is not None:
            try:
                c = calloc_fn(3)
                break
            except Exception:
                c = None

    prog = pq.QProg()

    h_gate = getattr(pq, "H")
    cnot_gate = getattr(pq, "CNOT", None)
    if cnot_gate is None:
        cnot_gate = getattr(pq, "CX")

    for gate in (h_gate(q[0]), cnot_gate(q[0], q[1]), h_gate(q[0])):
        try:
            result = prog << gate
            if result is not None:
                prog = result
        except Exception:
            insert_fn = getattr(prog, "insert")
            result = insert_fn(gate)
            if result is not None:
                prog = result

    apply_op_back._qpanda_machine = machine
    apply_op_back._qpanda_qubits = q
    apply_op_back._qpanda_cbits = c

    for conv_name in (
        "qprog_to_dag",
        "QProgToDAG",
        "prog_to_dag",
        "convert_qprog_to_dag",
        "circuit_to_dag",
    ):
        conv_fn = getattr(pq, conv_name, None)
        if conv_fn is not None:
            try:
                return conv_fn(prog)
            except Exception:
                pass

    for meth_name in ("to_dag", "toDAG", "to_DAG"):
        meth = getattr(prog, meth_name, None)
        if meth is not None:
            try:
                return meth()
            except Exception:
                pass

    return prog
