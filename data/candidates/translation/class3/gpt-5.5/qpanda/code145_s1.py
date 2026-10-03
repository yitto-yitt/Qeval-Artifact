# EVAL_META: task_id=145, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def qft_inverse(n):
    circuit = pq.QCircuit()

    def add_gate(gate):
        nonlocal circuit
        try:
            circuit = circuit << gate
        except Exception:
            circuit.insert(gate)

    def controlled_phase(control, target, angle):
        if hasattr(pq, "CR"):
            return pq.CR(control, target, angle)
        if hasattr(pq, "CP"):
            return pq.CP(control, target, angle)
        if hasattr(pq, "CU1"):
            return pq.CU1(control, target, angle)
        raise AttributeError("No controlled phase gate available in pyqpanda3.core")

    qubits = list(range(n))

    for i in range(n // 2):
        add_gate(pq.SWAP(qubits[i], qubits[n - i - 1]))

    for j in range(n):
        add_gate(pq.H(qubits[j]))
        for k in range(j + 1, n):
            add_gate(controlled_phase(qubits[k], qubits[j], -math.pi / (2 ** (k - j))))

    return circuit
