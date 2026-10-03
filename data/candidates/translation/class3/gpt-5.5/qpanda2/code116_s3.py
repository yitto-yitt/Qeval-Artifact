# EVAL_META: task_id=116, framework=qpanda2, class=3
import math
import atexit
import pyqpanda as pq

_MAX_QUBITS = 64
machine = pq.CPUQVM()
try:
    machine.set_configure(_MAX_QUBITS, _MAX_QUBITS)
except Exception:
    pass
machine.init_qvm()
q = machine.qAlloc_many(_MAX_QUBITS)
atexit.register(machine.finalize)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n > len(q):
        raise ValueError("Pauli string is longer than the globally allocated qubit register.")

    circuit = pq.QCircuit()

    for qi in range(n):
        circuit.insert(pq.RZ(q[qi], 0.0))

    active = []
    for qi in range(n):
        p = pauli_string[n - 1 - qi]
        if p == "I":
            continue
        if p not in ("X", "Y", "Z"):
            raise ValueError("Invalid Pauli character.")
        active.append((qi, p))

    for qi, p in active:
        if p == "X":
            circuit.insert(pq.H(q[qi]))
        elif p == "Y":
            circuit.insert(pq.RX(q[qi], math.pi / 2.0))

    active_qubits = [qi for qi, _ in active]

    if len(active_qubits) == 1:
        circuit.insert(pq.RZ(q[active_qubits[0]], 2.0 * time))
    elif len(active_qubits) > 1:
        pairs = list(zip(active_qubits[:-1], active_qubits[1:]))
        for control, target in pairs:
            circuit.insert(pq.CNOT(q[control], q[target]))
        circuit.insert(pq.RZ(q[active_qubits[-1]], 2.0 * time))
        for control, target in reversed(pairs):
            circuit.insert(pq.CNOT(q[control], q[target]))

    for qi, p in reversed(active):
        if p == "X":
            circuit.insert(pq.H(q[qi]))
        elif p == "Y":
            circuit.insert(pq.RX(q[qi], -math.pi / 2.0))

    return circuit
