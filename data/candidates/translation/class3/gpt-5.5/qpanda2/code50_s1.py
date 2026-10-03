# EVAL_META: task_id=50, framework=qpanda2, class=3
import operator
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit

    pos = operator.index(position)

    def _same(a, b):
        try:
            return a == b
        except Exception:
            return False

    def _call_first(obj, names):
        for name in names:
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    return method()
                except TypeError:
                    pass
        raise AttributeError

    def _size(obj):
        for name in (
            "__len__",
            "size",
            "get_size",
            "getSize",
            "get_node_num",
            "getNodeNum",
            "get_qgate_num",
            "getQGateNum",
        ):
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    return int(method())
                except Exception:
                    pass
        return None

    def _next_iter(it):
        for name in ("get_next", "getNext", "next"):
            method = getattr(it, name, None)
            if callable(method):
                try:
                    return method()
                except TypeError:
                    pass
        try:
            return next(it)
        except Exception:
            pass
        raise AttributeError

    def _delete_node(container, it):
        args = [it]
        for name in ("get_node", "getNode"):
            method = getattr(it, name, None)
            if callable(method):
                try:
                    args.append(method())
                    break
                except Exception:
                    pass

        for name in (
            "deleteQNode",
            "delete_QNode",
            "delete_qnode",
            "deleteNode",
            "delete_node",
            "delQNode",
            "erase",
            "remove",
        ):
            method = getattr(container, name, None)
            if callable(method):
                for arg in args:
                    try:
                        method(arg)
                        return
                    except Exception:
                        pass

        for name in (
            "deleteQNode",
            "delete_QNode",
            "delete_qnode",
            "deleteNode",
            "delete_node",
            "delQNode",
        ):
            func = globals().get(name)
            if callable(func):
                for arg in args:
                    try:
                        func(container, arg)
                        return
                    except Exception:
                        pass

        raise AttributeError("Cannot delete node from circuit")

    known_size = _size(circuit)
    iters = []

    try:
        begin = _call_first(circuit, ("begin", "getFirstNodeIter", "get_first_node_iter"))
        end = _call_first(circuit, ("end", "getEndNodeIter", "get_end_node_iter"))
        it = begin
        guard = 0
        while not _same(it, end):
            iters.append(it)
            it = _next_iter(it)
            guard += 1
            if known_size is not None and guard >= known_size:
                break
            if guard > 100000:
                break
    except Exception:
        iters = []
        try:
            first = _call_first(circuit, ("getFirstNodeIter", "get_first_node_iter", "begin"))
            last = _call_first(circuit, ("getLastNodeIter", "get_last_node_iter"))
            it = first
            if known_size is not None:
                for _ in range(max(known_size, 0)):
                    iters.append(it)
                    if _same(it, last):
                        break
                    it = _next_iter(it)
            else:
                guard = 0
                while True:
                    iters.append(it)
                    if _same(it, last):
                        break
                    it = _next_iter(it)
                    guard += 1
                    if guard > 100000:
                        break
        except Exception:
            pass

    if pos < 0:
        pos += len(iters)

    if pos < 0 or pos >= len(iters):
        raise IndexError("list assignment index out of range")

    _delete_node(circuit, iters[pos])
    return circuit

machine.finalize()
