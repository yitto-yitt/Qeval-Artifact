# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *
import operator

machine = CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    try:
        idx = operator.index(position)
    except TypeError:
        idx = int(position)

    data = getattr(circuit, "data", None)
    if data is not None:
        try:
            del data[idx]
            return circuit
        except (TypeError, AttributeError):
            pass

    try:
        del circuit[idx]
        return circuit
    except (TypeError, AttributeError, KeyError):
        pass

    pop = getattr(circuit, "pop", None)
    if callable(pop):
        try:
            pop(idx)
            return circuit
        except (TypeError, AttributeError):
            pass

    for name in ("remove_gate", "delete_gate", "erase_gate", "remove_qgate", "delete_qgate"):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(idx)
                return circuit
            except TypeError:
                pass

    def _call_first(obj):
        for name in ("begin", "getFirstNodeIter", "get_first_node_iter"):
            method = getattr(obj, name, None)
            if callable(method):
                return method()
        raise AttributeError("circuit has no node iterator begin method")

    def _call_end(obj):
        for name in ("end", "getEndNodeIter", "get_end_node_iter"):
            method = getattr(obj, name, None)
            if callable(method):
                return method()
        raise AttributeError("circuit has no node iterator end method")

    def _next_iter(iterator):
        for name in ("getNext", "get_next", "next", "__next__"):
            method = getattr(iterator, name, None)
            if callable(method):
                return method()
        return next(iterator)

    def _delete_iter(obj, iterator):
        for name in ("deleteQNode", "delete_qnode", "delete_node", "delete", "erase", "remove"):
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    method(iterator)
                    return True
                except TypeError:
                    pass
        for name in ("deleteQNode", "delete_qnode", "delete_node"):
            func = globals().get(name)
            if callable(func):
                try:
                    func(obj, iterator)
                    return True
                except TypeError:
                    try:
                        func(iterator)
                        return True
                    except TypeError:
                        pass
        return False

    begin = _call_first(circuit)
    end = _call_end(circuit)

    if idx < 0:
        count = 0
        iterator = begin
        while iterator != end:
            count += 1
            iterator = _next_iter(iterator)
        idx += count

    if idx < 0:
        raise IndexError("position out of range")

    iterator = begin
    for _ in range(idx):
        if iterator == end:
            raise IndexError("position out of range")
        iterator = _next_iter(iterator)

    if iterator == end:
        raise IndexError("position out of range")

    if not _delete_iter(circuit, iterator):
        raise AttributeError("unable to remove a gate from this circuit type")

    return circuit

machine.finalize()
