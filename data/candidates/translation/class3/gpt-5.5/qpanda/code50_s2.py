# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    try:
        pos = position.__index__()
    except Exception:
        pos = int(position)

    try:
        del circuit.data[pos]
        return circuit
    except Exception:
        pass

    try:
        data = circuit.data()
        del data[pos]
        return circuit
    except Exception:
        pass

    try:
        del circuit[pos]
        return circuit
    except Exception:
        pass

    def _count(obj):
        try:
            return len(obj)
        except Exception:
            pass
        for name in (
            "size", "get_size", "getSize", "node_count", "get_node_count",
            "getNodeCount", "get_qgate_num", "getQGateNum", "get_gate_count",
            "getGateCount"
        ):
            try:
                value = getattr(obj, name)
                value = value() if callable(value) else value
                return int(value)
            except Exception:
                pass
        for name in ("count_gate", "count_qgate_num", "get_qgate_num"):
            try:
                return int(globals()[name](obj))
            except Exception:
                pass
        return None

    def _delete_node(obj, node):
        for name in (
            "delete_node", "deleteNode", "delete_qnode", "deleteQNode",
            "erase", "remove_node", "removeNode"
        ):
            try:
                getattr(obj, name)(node)
                return True
            except Exception:
                pass
        for name in ("delete", "remove", "erase"):
            try:
                getattr(node, name)()
                return True
            except Exception:
                pass
        return False

    cnt = _count(circuit)
    norm_pos = pos
    if cnt is not None and norm_pos < 0:
        norm_pos += cnt

    for name in (
        "delete_node_by_index", "deleteNodeByIndex", "delete_gate_by_index",
        "deleteGateByIndex", "remove_gate_by_index", "removeGateByIndex",
        "remove_at", "removeAt", "erase_at", "eraseAt", "delete_at", "deleteAt"
    ):
        try:
            getattr(circuit, name)(norm_pos)
            return circuit
        except Exception:
            pass

    for name in (
        "get_node_iter_by_index", "getNodeIterByIndex", "get_node_by_index",
        "getNodeByIndex"
    ):
        try:
            node = getattr(circuit, name)(norm_pos)
            if _delete_node(circuit, node):
                return circuit
        except Exception:
            pass

    def _first(obj):
        for name in ("begin", "get_first_node_iter", "getFirstNodeIter", "get_first_node", "getFirstNode"):
            try:
                return getattr(obj, name)()
            except Exception:
                pass
        return None

    def _end(obj):
        for name in ("end", "get_end_node_iter", "getEndNodeIter"):
            try:
                return getattr(obj, name)()
            except Exception:
                pass
        return None

    def _next(obj, it):
        for name in ("get_next", "getNext", "next", "__next__", "get_next_node_iter", "getNextNodeIter"):
            try:
                return getattr(it, name)()
            except Exception:
                pass
        for name in ("get_next_node_iter", "getNextNodeIter"):
            try:
                return getattr(obj, name)(it)
            except Exception:
                pass
        return None

    first = _first(circuit)
    if first is not None:
        end = _end(circuit)
        nodes = []
        it = first
        limit = cnt if cnt is not None and cnt >= 0 else 100000
        for _ in range(limit):
            try:
                if end is not None and it == end:
                    break
            except Exception:
                pass
            nodes.append(it)
            nxt = _next(circuit, it)
            if nxt is None:
                break
            try:
                if nxt == it:
                    break
            except Exception:
                pass
            it = nxt
        if cnt is None and pos < 0:
            norm_pos = len(nodes) + pos
        if 0 <= norm_pos < len(nodes):
            if _delete_node(circuit, nodes[norm_pos]):
                return circuit

    try:
        ops = list(circuit)
        idx = pos if pos >= 0 else len(ops) + pos
        if idx < 0 or idx >= len(ops):
            raise IndexError("position out of range")
        new_circuit = circuit.__class__()
        for i, op in enumerate(ops):
            if i == idx:
                continue
            inserted = False
            for name in ("insert", "append", "push_back", "pushBack", "pushBackNode"):
                try:
                    getattr(new_circuit, name)(op)
                    inserted = True
                    break
                except Exception:
                    pass
            if not inserted:
                new_circuit << op
        return new_circuit
    except Exception:
        pass

    raise IndexError("position out of range")
