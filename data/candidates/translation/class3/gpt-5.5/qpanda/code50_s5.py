# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit

    try:
        del circuit[position]
        return circuit
    except Exception:
        pass

    pos = int(position)

    def _length(obj):
        try:
            return len(obj)
        except Exception:
            pass
        for name in ("size", "count", "node_count", "get_node_count"):
            attr = getattr(obj, name, None)
            if attr is not None:
                try:
                    return int(attr() if callable(attr) else attr)
                except Exception:
                    pass
        return None

    n = _length(circuit)
    if pos < 0 and n is not None:
        pos += n

    for name in ("remove_gate", "remove_node_by_index", "delete_node_by_index", "erase_node_by_index", "remove_at", "erase_at", "pop"):
        attr = getattr(circuit, name, None)
        if attr is not None:
            try:
                attr(pos)
                return circuit
            except Exception:
                pass

    if hasattr(circuit, "begin"):
        it = circuit.begin()
        for _ in range(pos):
            advanced = False
            for name in ("get_next", "next"):
                attr = getattr(it, name, None)
                if attr is not None:
                    try:
                        nxt = attr()
                        if nxt is not None:
                            it = nxt
                        advanced = True
                        break
                    except Exception:
                        pass
            if not advanced:
                try:
                    it = next(it)
                    advanced = True
                except Exception:
                    pass
            if not advanced:
                raise IndexError("position out of range")

        for name in ("delete_node", "erase", "remove_node", "remove", "delete"):
            attr = getattr(circuit, name, None)
            if attr is not None:
                try:
                    attr(it)
                    return circuit
                except Exception:
                    pass
                try:
                    node = it.get_node()
                    attr(node)
                    return circuit
                except Exception:
                    pass

    for name in ("remove", "erase", "delete_node"):
        attr = getattr(circuit, name, None)
        if attr is not None:
            try:
                attr(pos)
                return circuit
            except Exception:
                pass

    raise AttributeError("Unable to remove gate at the specified position from the provided pyQPanda3 circuit")
