# EVAL_META: task_id=36, framework=qpanda, class=3
import pyqpanda3.core as pq

_bv_function_refs = []

def bv_function(s):
    n = len(s)

    def new_circuit():
        try:
            return pq.QCircuit(n + 1)
        except Exception:
            return pq.QCircuit()

    def cnot_gate(control, target):
        if hasattr(pq, "CNOT"):
            return pq.CNOT(control, target)
        if hasattr(pq, "CX"):
            return pq.CX(control, target)
        return pq.X(target).control([control])

    circuit = new_circuit()

    try:
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                circuit << cnot_gate(index, n)
        return circuit
    except Exception:
        pass

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    qubits = machine.qAlloc_many(n + 1)

    circuit = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << cnot_gate(qubits[index], qubits[n])

    _bv_function_refs.append((machine, qubits))
    return circuit
