# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    if n < 5:
        raise IndexError("Circuit requires at least 5 qubits")

    hgate = globals().get("H")
    cnot = globals().get("CNOT")
    if cnot is None:
        cnot = globals().get("CX")

    def make_circuit(with_size=True):
        if with_size:
            try:
                return QCircuit(n)
            except Exception:
                pass
        return QCircuit()

    def add_gate(circuit, gate):
        try:
            result = circuit << gate
            return circuit if result is None else result
        except Exception:
            for name in ("insert", "append", "push_back"):
                method = getattr(circuit, name, None)
                if callable(method):
                    result = method(gate)
                    return circuit if result is None else result
            raise

    try:
        qc = make_circuit(True)
        for gate in (cnot(2, 4), cnot(1, 3), hgate(2), hgate(1)):
            qc = add_gate(qc, gate)
        return qc
    except Exception:
        qvm = CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(qvm, name, None)
            if callable(method):
                method()
                break

        alloc_many = None
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            alloc_many = getattr(qvm, name, None)
            if callable(alloc_many):
                break

        if callable(alloc_many):
            qubits = alloc_many(n)
        else:
            alloc_one = None
            for name in ("qAlloc", "qalloc"):
                alloc_one = getattr(qvm, name, None)
                if callable(alloc_one):
                    break
            qubits = [alloc_one() for _ in range(n)]

        qc = make_circuit(False)
        for gate in (cnot(qubits[2], qubits[4]), cnot(qubits[1], qubits[3]), hgate(qubits[2]), hgate(qubits[1])):
            qc = add_gate(qc, gate)

        if not hasattr(inv_circuit, "_qvms"):
            inv_circuit._qvms = []
        inv_circuit._qvms.append(qvm)

        return qc
