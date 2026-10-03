# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *


def remove_gate_in_position(circuit, position):
    try:
        del circuit.data[position]
        return circuit
    except Exception:
        pass

    for name in ("remove_gate", "remove_qgate", "delete_gate", "delete_qgate", "erase", "remove", "pop"):
        method = getattr(circuit, name, None)
        if method is not None:
            try:
                result = method(position)
                return circuit if result is None else result
            except Exception:
                pass

    try:
        current = circuit.begin()
        if position < 0:
            try:
                n = len(circuit)
            except Exception:
                n = circuit.size()
            position = n + position
        for _ in range(position):
            if hasattr(current, "get_next"):
                current = current.get_next()
            elif hasattr(current, "next"):
                current = current.next()
            else:
                current = next(current)

        for name in ("delete_qnode", "deleteQNode", "delete_node", "remove_node", "erase", "remove"):
            method = getattr(circuit, name, None)
            if method is not None:
                try:
                    result = method(current)
                    return circuit if result is None else result
                except Exception:
                    pass
    except Exception:
        pass

    nodes = None
    try:
        nodes = list(circuit)
    except Exception:
        pass

    if nodes is None:
        for getter in ("get_nodes", "nodes", "get_qgate_list", "get_gate_list", "instructions"):
            method = getattr(circuit, getter, None)
            if method is not None:
                try:
                    nodes = list(method())
                    break
                except Exception:
                    pass

    if nodes is None:
        try:
            n = len(circuit)
            nodes = [circuit[i] for i in range(n)]
        except Exception:
            try:
                n = circuit.size()
                nodes = [circuit[i] for i in range(n)]
            except Exception as exc:
                raise AttributeError("Unable to remove gate from the provided pyQPanda circuit") from exc

    del nodes[position]

    target = circuit
    cleared = False
    for name in ("clear", "reset"):
        method = getattr(target, name, None)
        if method is not None:
            try:
                method()
                cleared = True
                break
            except Exception:
                pass

    if not cleared:
        target = type(circuit)()

    for node in nodes:
        appended = False
        try:
            target << node
            appended = True
        except Exception:
            pass
        if not appended:
            for name in ("insert", "append", "push_back"):
                method = getattr(target, name, None)
                if method is not None:
                    try:
                        method(node)
                        appended = True
                        break
                    except Exception:
                        pass
        if not appended:
            raise AttributeError("Unable to rebuild the pyQPanda circuit after removing the gate")

    return target
