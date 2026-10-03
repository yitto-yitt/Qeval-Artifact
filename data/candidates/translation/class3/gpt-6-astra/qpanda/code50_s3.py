# EVAL_META: task_id=50, framework=qpanda, class=3
from operator import index
from pyqpanda3.core import QProg


def remove_gate_in_position(circuit, position):
    position = index(position)

    if hasattr(type(circuit), "__delitem__"):
        del circuit[position]
        return circuit

    if hasattr(circuit, "get_first_node_iter"):
        nodes = []
        node = circuit.get_first_node_iter()
        end = circuit.get_end_node_iter()
        while node != end:
            nodes.append(node)
            node = node.get_next()

        selected = nodes[position]
        for name in ("delete_qnode", "erase", "remove_node", "remove"):
            method = getattr(circuit, name, None)
            if method is not None:
                method(selected)
                return circuit

    try:
        size = len(circuit)
    except TypeError:
        for name in ("get_node_count", "get_node_num"):
            method = getattr(circuit, name, None)
            if method is not None:
                size = method()
                break
        else:
            size = sum(1 for _ in circuit)

    if position < 0:
        position += size
    if not 0 <= position < size:
        raise IndexError("circuit instruction index out of range")

    for name in ("remove", "remove_node", "delete_node", "erase", "pop"):
        method = getattr(circuit, name, None)
        if method is not None:
            method(position)
            return circuit

    raise TypeError("The circuit does not support instruction deletion")
