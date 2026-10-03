# EVAL_META: task_id=50, framework=qpanda, class=3
import operator
from pyqpanda3.core import QProg, QCircuit


def remove_gate_in_position(circuit, position):
    if hasattr(type(circuit), "__delitem__"):
        del circuit[position]
        return circuit

    position = operator.index(position)

    if all(
        hasattr(circuit, name)
        for name in ("get_first_node_iter", "get_end_node_iter", "delete_qnode")
    ):
        nodes = []
        node = circuit.get_first_node_iter()
        end = circuit.get_end_node_iter()
        while node != end:
            nodes.append(node)
            node = node.get_next()
        circuit.delete_qnode(nodes[position])
        return circuit

    size = None
    try:
        size = len(circuit)
    except TypeError:
        for name in ("size", "get_node_num", "get_node_count"):
            member = getattr(circuit, name, None)
            if member is not None:
                size = operator.index(member() if callable(member) else member)
                break

    if size is not None:
        if position < 0:
            position += size
        if not 0 <= position < size:
            raise IndexError("circuit instruction index out of range")
    elif position < 0:
        raise IndexError("Cannot resolve a negative instruction index")

    for name in ("remove", "remove_node", "delete_node", "erase", "delete_qnode"):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(position)
            except TypeError:
                continue
            return circuit

    raise TypeError("The circuit does not expose an instruction-deletion API")
