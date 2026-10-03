# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_GLOBAL_QUBITS = machine.qAlloc_many(64)

def remove_gate_in_position(circuit, position):
    pos = int(position)

    if hasattr(circuit, "data"):
        del circuit.data[pos]
        return circuit

    try:
        del circuit[pos]
        return circuit
    except Exception:
        pass

    for name in ("pop", "remove_at", "erase_at", "delete_at", "delete_node_at"):
        method = getattr(circuit, name, None)
        if method is not None:
            try:
                method(pos)
                return circuit
            except Exception:
                pass

    def _begin(obj):
        for name in ("begin", "getFirstNodeIter", "get_first_node_iter"):
            method = getattr(obj, name, None)
            if method is not None:
                try:
                    return method()
                except Exception:
                    pass
        return None

    def _end(obj):
        for name in ("end", "getEndNodeIter", "get_end_node_iter"):
            method = getattr(obj, name, None)
            if method is not None:
                try:
                    return method()
                except Exception:
                    pass
        return None

    def _next(it):
        for name in ("get_next", "next", "__next__"):
            method = getattr(it, name, None)
            if method is not None:
                return method()
        raise TypeError("Iterator does not support advancing")

    begin = _begin(circuit)
    end = _end(circuit)

    if begin is not None:
        if pos < 0:
            count = 0
            it = begin
            if end is not None:
                while it != end:
                    count += 1
                    it = _next(it)
            else:
                while True:
                    try:
                        it = _next(it)
                        count += 1
                    except Exception:
                        break
            pos += count

        if pos < 0:
            raise IndexError("position out of range")

        it = begin
        for _ in range(pos):
            if end is not None and it == end:
                raise IndexError("position out of range")
            it = _next(it)

        if end is not None and it == end:
            raise IndexError("position out of range")

        for name in ("delete", "erase", "remove", "delete_node", "deleteQNode", "delete_qnode", "remove_node", "removeQNode", "remove_qnode"):
            method = getattr(circuit, name, None)
            if method is not None:
                try:
                    method(it)
                    return circuit
                except Exception:
                    pass

    raise AttributeError("Unable to remove gate at the specified position from this circuit object")

machine.finalize()
