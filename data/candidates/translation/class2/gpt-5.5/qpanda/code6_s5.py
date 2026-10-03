# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep(num_qubits):
    def add(prog, node):
        try:
            prog << node
        except TypeError:
            prog.insert(node)

    try:
        prog = QProg()
        if num_qubits > 0:
            add(prog, X(0))
            for i in range(1, num_qubits):
                add(prog, X(i))
                add(prog, X(i))
        return prog
    except Exception:
        qvm = CPUQVM()
        for init_name in ("init_qvm", "init"):
            init = getattr(qvm, init_name, None)
            if init is not None:
                try:
                    init()
                except TypeError:
                    pass
                break

        qubits = None
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            alloc = getattr(qvm, alloc_name, None)
            if alloc is not None:
                qubits = alloc(num_qubits)
                break

        if qubits is None:
            single_alloc = None
            for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
                single_alloc = getattr(qvm, alloc_name, None)
                if single_alloc is not None:
                    break
            qubits = [single_alloc() for _ in range(num_qubits)]

        prog = QProg()
        if num_qubits > 0:
            add(prog, X(qubits[0]))
            for i in range(1, num_qubits):
                add(prog, X(qubits[i]))
                add(prog, X(qubits[i]))

        if not hasattr(create_state_prep, "_qvms"):
            create_state_prep._qvms = []
        create_state_prep._qvms.append(qvm)
        return prog
