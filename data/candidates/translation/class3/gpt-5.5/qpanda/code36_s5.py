# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import *

def bv_function(s):
    n = len(s)
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(n + 1)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(n + 1)
    elif hasattr(machine, "qAllocMany"):
        qubits = machine.qAllocMany(n + 1)
    elif hasattr(machine, "allocate_qubits"):
        qubits = machine.allocate_qubits(n + 1)
    else:
        alloc_one = (
            getattr(machine, "qAlloc", None)
            or getattr(machine, "qalloc", None)
            or getattr(machine, "allocate_qubit", None)
        )
        qubits = [alloc_one() for _ in range(n + 1)]

    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qubits[index], qubits[n])

    if not hasattr(bv_function, "_machines"):
        bv_function._machines = []
    bv_function._machines.append(machine)
    return qc
