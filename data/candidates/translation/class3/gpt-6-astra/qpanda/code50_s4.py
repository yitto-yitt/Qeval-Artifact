# EVAL_META: task_id=50, framework=qpanda, class=3
import operator
import pyqpanda3.core as pq


def remove_gate_in_position(circuit, position):
    if hasattr(type(circuit), "__delitem__"):
        del circuit[position]
        return circuit

    if all(hasattr(circuit, name) for name in
           ("get_first_node", "get_end_node", "delete_node")):
        nodes = []
        node = circuit.get_first_node()
        end = circuit.get_end_node()
        while node != end:
            nodes.append(node)
            node = node.get_next()

        if isinstance(position, slice):
            indices = range(*position.indices(len(nodes)))
            for index in sorted(indices, reverse=True):
                circuit.delete_node(nodes[index])
        else:
            circuit.delete_node(nodes[operator.index(position)])
        return circuit

    position = operator.index(position)
    if position < 0:
        position += len(circuit)
        if position < 0:
            raise IndexError("circuit instruction index out of range")

    for name in ("delete_node", "remove", "erase", "pop", "delete"):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(position)
            except TypeError:
                continue
            return circuit

    raise TypeError("The circuit does not expose a supported instruction-deletion API")
