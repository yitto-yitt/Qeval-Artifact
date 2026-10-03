# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    pos = int(position)

    for attr in ("data", "gates", "instructions", "operations", "ops", "nodes"):
        try:
            seq = getattr(circuit, attr)
        except Exception:
            continue
        if callable(seq):
            continue
        try:
            del seq[pos]
            return circuit
        except Exception:
            pass

    try:
        del circuit[pos]
        return circuit
    except Exception:
        pass

    def _count_nodes(obj):
        try:
            return len(obj)
        except Exception:
            pass
        for name in (
            "size", "count", "node_count", "get_node_count", "getNodeCount",
            "gate_count", "get_gate_count", "getGateCount", "get_qgate_num",
            "getQGateNum", "qgate_num", "get_qgate_count", "getQGateCount"
        ):
            meth = getattr(obj, name, None)
            if callable(meth):
                try:
                    return int(meth())
                except Exception:
                    pass
        for name in (
            "get_qgate_num", "count_qgate_num", "get_qgate_count",
            "get_node_count", "getQGateNum"
        ):
            func = globals().get(name)
            if callable(func):
                try:
                    return int(func(obj))
                except Exception:
                    pass
        return None

    count = _count_nodes(circuit)
    idx = pos
    if idx < 0 and count is not None:
        idx += count

    for name in (
        "remove_gate_at", "removeGateAt", "delete_gate_at", "deleteGateAt",
        "erase_gate_at", "eraseGateAt", "remove_gate", "removeGate",
        "delete_gate", "deleteGate", "erase_gate", "eraseGate", "pop_gate",
        "popGate", "remove_node_at", "removeNodeAt", "delete_node_at",
        "deleteNodeAt", "erase_node_at", "eraseNodeAt", "remove", "erase",
        "delete", "delete_node", "deleteNode"
    ):
        meth = getattr(circuit, name, None)
        if callable(meth):
            try:
                meth(idx)
                return circuit
            except Exception:
                pass

    def _first_iter(obj):
        for name in (
            "begin", "get_first_node_iter", "getFirstNodeIter",
            "get_first_node", "getFirstNode", "first_node_iter",
            "firstNodeIter"
        ):
            meth = getattr(obj, name, None)
            if callable(meth):
                try:
                    return meth()
                except Exception:
                    pass
        return None

    def _end_iter(obj):
        for name in (
            "end", "get_end_node_iter", "getEndNodeIter",
            "get_last_node_iter", "getLastNodeIter"
        ):
            meth = getattr(obj, name, None)
            if callable(meth):
                try:
                    return meth()
                except Exception:
                    pass
        return None

    def _next_iter(obj, it):
        for name in (
            "get_next_node_iter", "getNextNodeIter", "get_next_iter",
            "getNextIter", "next_node_iter", "nextNodeIter"
        ):
            meth = getattr(obj, name, None)
            if callable(meth):
                try:
                    return meth(it)
                except Exception:
                    pass
        for name in (
            "get_next", "getNext", "get_next_iter", "getNextIter",
            "next", "__next__"
        ):
            meth = getattr(it, name, None)
            if callable(meth):
                try:
                    return meth()
                except Exception:
                    pass
        return None

    it = _first_iter(circuit)
    if it is not None:
        if idx < 0:
            end_it = _end_iter(circuit)
            all_iters = []
            cur = it
            guard = 0
            while cur is not None and guard < 100000:
                if end_it is not None:
                    try:
                        if cur == end_it:
                            break
                    except Exception:
                        pass
                all_iters.append(cur)
                nxt = _next_iter(circuit, cur)
                if nxt is None:
                    break
                try:
                    if nxt == cur:
                        break
                except Exception:
                    pass
                cur = nxt
                guard += 1
            idx = len(all_iters) + idx
            if 0 <= idx < len(all_iters):
                it = all_iters[idx]
            else:
                raise IndexError("position out of range")
        else:
            for _ in range(idx):
                nxt = _next_iter(circuit, it)
                if nxt is None:
                    raise IndexError("position out of range")
                it = nxt

        for name in (
            "delete_node", "deleteNode", "delete_qnode", "deleteQNode",
            "delete_qgate", "deleteQGate", "remove_node", "removeNode",
            "erase_node", "eraseNode", "remove", "erase", "delete"
        ):
            meth = getattr(circuit, name, None)
            if callable(meth):
                try:
                    meth(it)
                    return circuit
                except Exception:
                    pass

    nodes = None
    try:
        nodes = list(circuit)
    except Exception:
        if count is not None:
            tmp = []
            ok = True
            for i in range(count):
                try:
                    tmp.append(circuit[i])
                except Exception:
                    ok = False
                    break
            if ok:
                nodes = tmp

    if nodes is not None:
        if pos < 0:
            pos += len(nodes)
        if not (0 <= pos < len(nodes)):
            raise IndexError("position out of range")
        kept = [node for i, node in enumerate(nodes) if i != pos]

        def _append(obj, node):
            for name in ("insert", "append", "push_back", "pushBack", "add", "add_node", "addNode"):
                meth = getattr(obj, name, None)
                if callable(meth):
                    try:
                        meth(node)
                        return True
                    except Exception:
                        pass
            try:
                obj << node
                return True
            except Exception:
                return False

        try:
            new_circuit = circuit.__class__()
            for node in kept:
                if not _append(new_circuit, node):
                    raise TypeError
            return new_circuit
        except Exception:
            pass

        for name in ("clear", "reset", "clear_nodes", "clearNodes"):
            meth = getattr(circuit, name, None)
            if callable(meth):
                try:
                    meth()
                    for node in kept:
                        if not _append(circuit, node):
                            raise TypeError
                    return circuit
                except Exception:
                    pass

    raise AttributeError("the provided circuit object does not support gate removal by position")
