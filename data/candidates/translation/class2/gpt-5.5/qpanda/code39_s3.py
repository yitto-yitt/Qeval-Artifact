# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3.core as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(n)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(n)
    else:
        alloc = machine.qAlloc if hasattr(machine, "qAlloc") else machine.qalloc
        qubits = [alloc() for _ in range(n)]

    prog = pq.QProg()
    for q in qubits:
        gate = pq.H(q)
        if hasattr(prog, "insert"):
            prog.insert(gate)
        else:
            prog = prog << gate

    executed = False
    for run_name in ("directly_run", "run", "execute"):
        if hasattr(machine, run_name):
            try:
                getattr(machine, run_name)(prog)
                executed = True
                break
            except TypeError:
                continue
    if not executed:
        raise RuntimeError("Unable to execute quantum program with pyQPanda3 CPUQVM.")

    for state_name in (
        "get_qstate",
        "get_qstate_vector",
        "get_statevector",
        "get_state_vector",
        "get_state",
        "getQState",
        "getQStateVector",
    ):
        if hasattr(machine, state_name):
            getter = getattr(machine, state_name)
            try:
                return getter()
            except TypeError:
                return getter(prog)

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 CPUQVM.")
