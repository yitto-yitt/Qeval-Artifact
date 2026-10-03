# EVAL_META: task_id=50, framework=qpanda, class=3
from operator import index
from pyqpanda3.core import QProg


def remove_gate_in_position(circuit, position):
    position = index(position)

    if hasattr(type(circuit), "__delitem__"):
        del circuit[position]
        return circuit

    first = getattr(circuit, "get_first_node_iter", None)
    end = getattr(circuit, "get_end_node_iter", None)
    delete = getattr(circuit, "delete_qnode", None)

    if first is None:
        first = getattr(circuit, "begin", None)
    if end is None:
        end = getattr(circuit, "end", None)

    if callable(first) and callable(end) and callable(delete):
        nodes = []
        current = first()
        stop = end()
        while current != stop:
            nodes.append(current)
            current = current.get_next()
        delete(nodes[position])
        return circuit

    size = None
    if hasattr(type(circuit), "__len__"):
        size = len(circuit)
    else:
        for name in ("size", "get_node_num", "get_node_count"):
            member = getattr(circuit, name, None)
            if member is not None:
                size = index(member() if callable(member) else member)
                break

    if size is not None:
        if position < 0:
            position += size
        if not 0 <= position < size:
            raise IndexError("circuit instruction index out of range")

    for name in ("remove", "remove_node", "delete_node", "erase", "pop"):
        remove = getattr(circuit, name, None)
        if callable(remove):
            remove(position)
            return circuit

    if size is not None and callable(getattr(circuit, "clear", None)):
        replacement = QProg()
        for instruction_index in range(size):
            if instruction_index != position:
                replacement << circuit[instruction_index]
        circuit.clear()
        circuit << replacement
        return circuit

    raise TypeError("The circuit does not expose an instruction-removal API")
