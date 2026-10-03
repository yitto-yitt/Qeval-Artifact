# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str):
        raise TypeError("pauli_string must be a string.")
    if not pauli_string or any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string must be a nonempty string of I, X, Y, Z.")

    angle = 2.0 * float(time)
    n = len(pauli_string)
    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for q in qubits[:n]:
        circuit << pq.I(q)

    active = []
    basis_changes = []
    for index, pauli in enumerate(reversed(pauli_string)):
        q = qubits[index]
        if pauli == "I":
            continue
        active.append(q)
        if pauli == "X":
            circuit << pq.H(q)
            basis_changes.append((q, "X"))
        elif pauli == "Y":
            circuit << pq.RX(q, math.pi / 2.0)
            basis_changes.append((q, "Y"))

    if active:
        target = active[-1]
        for control in active[:-1]:
            circuit << pq.CNOT(control, target)

        circuit << pq.RZ(target, angle)

        for control in reversed(active[:-1]):
            circuit << pq.CNOT(control, target)

        for q, pauli in reversed(basis_changes):
            if pauli == "X":
                circuit << pq.H(q)
            else:
                circuit << pq.RX(q, -math.pi / 2.0)
    else:
        circuit << pq.RZ(qubits[0], angle)
        circuit << pq.U1(qubits[0], -angle)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
