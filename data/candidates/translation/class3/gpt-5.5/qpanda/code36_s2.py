# EVAL_META: task_id=36, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *

def bv_function(s):
    n = len(s)

    qvm = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except TypeError:
                pass

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(qvm, alloc_name):
            qubits = getattr(qvm, alloc_name)(n + 1)
            break
    if qubits is None:
        qubits = [qvm.qAlloc() for _ in range(n + 1)]

    circuit = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            gate = pq.CNOT(qubits[index], qubits[n])
            if hasattr(circuit, "insert"):
                circuit.insert(gate)
            else:
                circuit = circuit << gate

    if not hasattr(bv_function, "_qvms"):
        bv_function._qvms = []
    bv_function._qvms.append(qvm)

    return circuit
