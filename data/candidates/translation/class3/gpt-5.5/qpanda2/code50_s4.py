# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)


def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit

    try:
        del circuit[position]
        return circuit
    except Exception:
        pass

    def _method_call(obj, names):
        for name in names:
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    return method()
                except TypeError:
                    continue
        raise AttributeError

    def _next_iter(iterator):
        for name in ("getNextIter", "get_next_iter", "next", "__next__"):
            method = getattr(iterator, name, None)
            if callable(method):
                result = method()
                return iterator if result is None else result
        raise AttributeError

    first = _method_call(circuit, ("getFirstNodeIter", "get_first_node_iter"))
    end = _method_call(circuit, ("getEndNodeIter", "get_end_node_iter"))

    if position < 0:
        it = first
        iterators = []
        while not (it == end):
            iterators.append(it)
            it = _next_iter(it)
        target_index = len(iterators) + position
        if target_index < 0 or target_index >= len(iterators):
            raise IndexError("gate index out of range")
        target = iterators[target_index]
    else:
        target = first
        for _ in range(position):
            if target == end:
                raise IndexError("gate index out of range")
            target = _next_iter(target)
        if target == end:
            raise IndexError("gate index out of range")

    for name in ("deleteQNode", "delete_qnode", "deleteNode", "delete_node", "erase"):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(target)
                return circuit
            except TypeError:
                continue

    raise AttributeError("the supplied circuit does not support node deletion")


machine.finalize()
