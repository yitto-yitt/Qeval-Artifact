# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        try:
            del circuit.data[position]
            return circuit
        except Exception:
            pass

    try:
        del circuit[position]
        return circuit
    except Exception:
        pass

    for name in (
        "pop",
        "remove_at",
        "erase_at",
        "delete_at",
        "remove_gate_at",
        "delete_gate_at",
        "remove_node_at",
        "delete_node_at",
        "remove",
        "erase",
        "delete",
    ):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(position)
                return circuit
            except Exception:
                pass

    items = None
    try:
        items = list(circuit)
    except Exception:
        items = None

    if items is not None:
        idx = position
        if idx < 0:
            idx += len(items)
        if idx < 0 or idx >= len(items):
            raise IndexError("position out of range")
        node = items[idx]

        for name in ("delete_node", "remove_node", "delete_gate", "remove_gate", "erase", "remove"):
            method = getattr(circuit, name, None)
            if callable(method):
                try:
                    method(node)
                    return circuit
                except Exception:
                    pass

        for clear_name in ("clear", "reset"):
            clear_method = getattr(circuit, clear_name, None)
            if callable(clear_method):
                try:
                    clear_method()
                    for i, item in enumerate(items):
                        if i == idx:
                            continue
                        try:
                            circuit = circuit << item
                        except Exception:
                            append_method = getattr(circuit, "append", None)
                            if callable(append_method):
                                append_method(item)
                            else:
                                insert_method = getattr(circuit, "insert", None)
                                if callable(insert_method):
                                    insert_method(item)
                                else:
                                    raise
                    return circuit
                except Exception:
                    pass

        constructors = [type(circuit)]
        try:
            if "prog" in type(circuit).__name__.lower():
                constructors.append(QProg)
            else:
                constructors.append(QCircuit)
        except Exception:
            pass

        for ctor in constructors:
            try:
                new_circuit = ctor()
                for i, item in enumerate(items):
                    if i == idx:
                        continue
                    try:
                        new_circuit = new_circuit << item
                    except Exception:
                        append_method = getattr(new_circuit, "append", None)
                        if callable(append_method):
                            append_method(item)
                        else:
                            insert_method = getattr(new_circuit, "insert", None)
                            if callable(insert_method):
                                insert_method(item)
                            else:
                                raise
                return new_circuit
            except Exception:
                pass

    try:
        idx = position
        if idx < 0:
            length = None
            for name in ("__len__", "size", "length", "get_qgate_num"):
                if name == "__len__":
                    try:
                        length = len(circuit)
                        break
                    except Exception:
                        continue
                method = getattr(circuit, name, None)
                if callable(method):
                    try:
                        length = method()
                        break
                    except Exception:
                        pass
            if length is not None:
                idx += length

        it = circuit.begin()
        for _ in range(idx):
            advanced = False
            for name in ("get_next", "next"):
                method = getattr(it, name, None)
                if callable(method):
                    try:
                        it = method()
                        advanced = True
                        break
                    except Exception:
                        pass
            if not advanced:
                for name in ("get_next_node_iter", "get_next_node"):
                    method = getattr(circuit, name, None)
                    if callable(method):
                        try:
                            it = method(it)
                            advanced = True
                            break
                        except Exception:
                            pass
            if not advanced:
                it = next(it)

        for name in ("delete_node", "remove_node", "erase", "delete", "remove"):
            method = getattr(circuit, name, None)
            if callable(method):
                try:
                    method(it)
                    return circuit
                except Exception:
                    pass
    except Exception:
        pass

    raise AttributeError("The supplied circuit object does not expose a supported gate-removal API.")
