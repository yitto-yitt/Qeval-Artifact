# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math

_QPANDA_TASK_116_MACHINES = []


def _task116_init_machine():
    machine = CPUQVM()
    for name in ("init_qvm", "init", "initQVM"):
        method = getattr(machine, name, None)
        if method is not None:
            try:
                method()
            except TypeError:
                method("")
            break
    _QPANDA_TASK_116_MACHINES.append(machine)
    return machine


def _task116_alloc_qubits(machine, n):
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        method = getattr(machine, name, None)
        if method is not None:
            return list(method(n))
    for name in ("qAlloc", "qalloc", "allocate_qubit"):
        method = getattr(machine, name, None)
        if method is not None:
            return [method() for _ in range(n)]
    raise RuntimeError("Unable to allocate qubits with pyQPanda3 CPUQVM.")


def _task116_insert(circuit, op):
    try:
        circuit << op
    except Exception:
        circuit.insert(op)
    return circuit


def _task116_rz(q, angle):
    try:
        return RZ(q, angle)
    except TypeError:
        return RZ(angle, q)


def _task116_h(q):
    return H(q)


def _task116_cnot(control, target):
    if "CNOT" in globals():
        try:
            return CNOT(control, target)
        except Exception:
            pass
    if "CX" in globals():
        try:
            return CX(control, target)
        except Exception:
            pass
    gate = X(target)
    return gate.control([control])


def synthesize_evolution_gate(pauli_string, time):
    pauli_string = str(pauli_string)
    num_qubits = len(pauli_string)

    machine = _task116_init_machine()
    qubits = _task116_alloc_qubits(machine, num_qubits)

    circuit = QCircuit()

    for qb in qubits:
        _task116_insert(circuit, _task116_rz(qb, 0.0))

    active = []
    for q_index, pauli in enumerate(reversed(pauli_string)):
        p = pauli.upper()
        if p == "I":
            continue
        if p == "X":
            _task116_insert(circuit, _task116_h(qubits[q_index]))
            active.append(q_index)
        elif p == "Y":
            _task116_insert(circuit, _task116_rz(qubits[q_index], -math.pi / 2.0))
            _task116_insert(circuit, _task116_h(qubits[q_index]))
            active.append(q_index)
        elif p == "Z":
            active.append(q_index)
        else:
            raise ValueError("Invalid Pauli string.")

    if active:
        for i in range(len(active) - 1):
            _task116_insert(circuit, _task116_cnot(qubits[active[i]], qubits[active[i + 1]]))

        _task116_insert(circuit, _task116_rz(qubits[active[-1]], 2.0 * float(time)))

        for i in range(len(active) - 2, -1, -1):
            _task116_insert(circuit, _task116_cnot(qubits[active[i]], qubits[active[i + 1]]))

    for q_index in reversed(active):
        p = pauli_string[num_qubits - 1 - q_index].upper()
        if p == "X":
            _task116_insert(circuit, _task116_h(qubits[q_index]))
        elif p == "Y":
            _task116_insert(circuit, _task116_h(qubits[q_index]))
            _task116_insert(circuit, _task116_rz(qubits[q_index], math.pi / 2.0))

    return circuit
