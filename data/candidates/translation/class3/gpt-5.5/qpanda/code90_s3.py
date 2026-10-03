# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    def _append(container, node):
        try:
            result = container << node
            return container if result is None else result
        except Exception:
            result = container.insert(node)
            return container if result is None else result

    def _controlled(node, controls):
        result = node.control(controls)
        return node if result is None else result

    machine = CPUQVM()
    for name in ("init_qvm", "init", "initQVM"):
        if hasattr(machine, name):
            getattr(machine, name)()
            break

    alloc = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(machine, name):
            alloc = getattr(machine, name)
            break
    if alloc is None:
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if name in globals():
                alloc = globals()[name]
                break

    q = alloc(4)
    controls = [q[0], q[3]]

    custom = QCircuit()
    custom = _append(custom, X(q[1]))
    custom = _append(custom, H(q[2]))

    prog = QProg()
    try:
        prog = _append(prog, _controlled(custom, controls))
    except Exception:
        prog = _append(prog, _controlled(X(q[1]), controls))
        prog = _append(prog, _controlled(H(q[2]), controls))

    if not hasattr(create_custom_controlled, "_resources"):
        create_custom_controlled._resources = []
    create_custom_controlled._resources.append((machine, q))
    return prog
