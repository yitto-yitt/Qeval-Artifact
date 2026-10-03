# EVAL_META: task_id=65, framework=qpanda, class=3
import pyqpanda3.core as pq
from math import pi

def QFT(n):
    n = int(n)

    machine = pq.CPUQVM()
    for _init_name in ("init", "init_qvm"):
        if hasattr(machine, _init_name):
            getattr(machine, _init_name)()
            break

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(n)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(n)
    elif hasattr(machine, "qAllocMany"):
        qubits = machine.qAllocMany(n)
    else:
        qubits = [machine.qAlloc() for _ in range(n)]

    if not hasattr(QFT, "_machines"):
        QFT._machines = []
    QFT._machines.append(machine)

    circuit = pq.QCircuit()

    def append_gate(gate):
        nonlocal circuit
        try:
            result = circuit.__lshift__(gate)
            if result is not None:
                circuit = result
        except Exception:
            circuit.insert(gate)

    def make_one_qubit_gate(names, qubit, angle=None):
        last_error = None
        for name in names:
            func = getattr(pq, name, None)
            if func is None:
                continue
            variants = ((qubit,) if angle is None else (qubit, angle),
                        (qubit,) if angle is None else (angle, qubit))
            for args in variants:
                try:
                    return func(*args)
                except Exception as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise AttributeError(names[0])

    def make_two_qubit_gate(names, q0, q1):
        last_error = None
        for name in names:
            func = getattr(pq, name, None)
            if func is None:
                continue
            try:
                return func(q0, q1)
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise AttributeError(names[0])

    def h_gate(q):
        return make_one_qubit_gate(("H", "Hadamard"), q)

    def rz_gate(q, angle):
        return make_one_qubit_gate(("RZ", "Rz"), q, angle)

    def cnot_gate(control, target):
        return make_two_qubit_gate(("CNOT", "CX"), control, target)

    def swap_gate(q0, q1):
        for name in ("SWAP", "Swap"):
            func = getattr(pq, name, None)
            if func is not None:
                try:
                    return func(q0, q1)
                except Exception:
                    pass
        return None

    def append_controlled_phase(control, target, angle):
        for name in ("CP", "CR", "CPhase", "CPHASE"):
            func = getattr(pq, name, None)
            if func is None:
                continue
            for args in ((control, target, angle), (angle, control, target)):
                try:
                    append_gate(func(*args))
                    return
                except Exception:
                    pass
        append_gate(rz_gate(target, angle / 2.0))
        append_gate(cnot_gate(control, target))
        append_gate(rz_gate(target, -angle / 2.0))
        append_gate(cnot_gate(control, target))
        append_gate(rz_gate(control, angle / 2.0))

    def append_swap(q0, q1):
        gate = swap_gate(q0, q1)
        if gate is not None:
            append_gate(gate)
        else:
            append_gate(cnot_gate(q0, q1))
            append_gate(cnot_gate(q1, q0))
            append_gate(cnot_gate(q0, q1))

    def swap_registers(size):
        for qubit in range(size // 2):
            append_swap(qubits[qubit], qubits[size - qubit - 1])

    def qft_rotations(size):
        if size == 0:
            return
        size -= 1
        append_gate(h_gate(qubits[size]))
        for qubit in range(size):
            append_controlled_phase(qubits[qubit], qubits[size], pi / (2 ** (size - qubit)))
        qft_rotations(size)

    qft_rotations(n)
    swap_registers(n)
    return circuit
