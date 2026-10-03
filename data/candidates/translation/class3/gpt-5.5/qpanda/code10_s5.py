# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *

def create_operator():
    machine = CPUQVM()

    for _name in ("init_qvm", "init", "initQVM"):
        _method = getattr(machine, _name, None)
        if callable(_method):
            try:
                _method()
                break
            except TypeError:
                continue

    def _alloc_many(_machine, _count, _many_names, _single_names):
        for _name in _many_names:
            _method = getattr(_machine, _name, None)
            if callable(_method):
                try:
                    return _method(_count)
                except TypeError:
                    pass
        _items = []
        for _ in range(_count):
            _allocated = None
            for _name in _single_names:
                _method = getattr(_machine, _name, None)
                if callable(_method):
                    try:
                        _allocated = _method()
                        break
                    except TypeError:
                        continue
            if _allocated is None:
                raise RuntimeError("Unable to allocate qubit/cbit in pyQPanda3.")
            _items.append(_allocated)
        return _items

    q = _alloc_many(
        machine,
        2,
        ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"),
        ("qAlloc", "qalloc", "qAllocOne", "qallocOne", "allocate_qubit"),
    )

    try:
        c = _alloc_many(
            machine,
            2,
            ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany", "allocate_cbits"),
            ("cAlloc", "calloc", "cAllocOne", "callocOne", "allocate_cbit"),
        )
    except Exception:
        c = None

    prog = QProg()
    prog << X(q[0])
    prog << X(q[1])

    if not hasattr(create_operator, "_qpanda_keepalive"):
        create_operator._qpanda_keepalive = []
    create_operator._qpanda_keepalive.append((machine, q, c))

    return prog
