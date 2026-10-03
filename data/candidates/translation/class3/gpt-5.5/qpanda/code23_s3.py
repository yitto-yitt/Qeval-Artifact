# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    try:
        oracle = QCircuit()
        gate = X(2)
        try:
            oracle << gate
        except Exception:
            oracle.insert(gate)
        return oracle
    except Exception:
        machine = CPUQVM()

        for init_name in ("init_qvm", "init", "initQVM"):
            init_method = getattr(machine, init_name, None)
            if init_method is not None:
                init_method()
                break

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
            alloc_method = getattr(machine, alloc_name, None)
            if alloc_method is not None:
                qubits = alloc_method(3)
                break

        if qubits is None:
            alloc_one = getattr(machine, "qAlloc")
            qubits = [alloc_one() for _ in range(3)]

        oracle = QCircuit()
        gate = X(qubits[2])
        try:
            oracle << gate
        except Exception:
            oracle.insert(gate)

        resources = getattr(dj_constant_oracle, "_resources", [])
        resources.append((machine, qubits))
        dj_constant_oracle._resources = resources

        return oracle
