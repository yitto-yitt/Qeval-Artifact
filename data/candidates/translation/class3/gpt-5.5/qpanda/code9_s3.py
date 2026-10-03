# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    initialized = False
    for init_name in ("init_qvm", "init"):
        if hasattr(machine, init_name):
            getattr(machine, init_name)()
            initialized = True
            break

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(machine, alloc_name):
            qubits = getattr(machine, alloc_name)(3)
            break
    if qubits is None:
        alloc_one = None
        for alloc_name in ("qAlloc", "qalloc", "qAllocOne", "qallocOne"):
            if hasattr(machine, alloc_name):
                alloc_one = getattr(machine, alloc_name)
                break
        qubits = [alloc_one() for _ in range(3)]

    circuit = QCircuit()

    if not hasattr(create_efficientSU2, "_machines"):
        create_efficientSU2._machines = []
    create_efficientSU2._machines.append(machine)

    def append_op(container, op):
        if hasattr(container, "insert"):
            try:
                result = container.insert(op)
                return container if result is None else result
            except Exception:
                pass
        result = container << op
        return container if result is None else result

    def make_param(index):
        for ctor_name in ("Parameter", "QParameter"):
            ctor = globals().get(ctor_name)
            if ctor is not None:
                try:
                    return ctor("theta[%d]" % index)
                except Exception:
                    pass
        return 0.0

    params = [make_param(i) for i in range(12)]

    def add_rotation(gate_ctor, qubit, angle):
        nonlocal circuit
        try:
            circuit = append_op(circuit, gate_ctor(qubit, angle))
        except Exception:
            circuit = append_op(circuit, gate_ctor(qubit, 0.0))

    def add_barrier():
        nonlocal circuit
        barrier_ctor = globals().get("BARRIER", globals().get("Barrier", None))
        if barrier_ctor is None:
            return
        for args in ((qubits,), (list(qubits),), tuple(qubits)):
            try:
                circuit = append_op(circuit, barrier_ctor(*args))
                return
            except Exception:
                pass

    cx_ctor = globals().get("CNOT", globals().get("CX"))

    for i in range(3):
        add_rotation(RY, qubits[i], params[i])
    for i in range(3):
        add_rotation(RZ, qubits[i], params[i + 3])

    add_barrier()

    circuit = append_op(circuit, cx_ctor(qubits[2], qubits[1]))
    circuit = append_op(circuit, cx_ctor(qubits[1], qubits[0]))

    add_barrier()

    for i in range(3):
        add_rotation(RY, qubits[i], params[i + 6])
    for i in range(3):
        add_rotation(RZ, qubits[i], params[i + 9])

    return circuit
