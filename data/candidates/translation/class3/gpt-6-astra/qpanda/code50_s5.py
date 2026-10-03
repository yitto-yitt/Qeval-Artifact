# EVAL_META: task_id=50, framework=qpanda, class=3
import operator
from pyqpanda3.core import QProg, QCircuit


def remove_gate_in_position(circuit, position):
    position = operator.index(position)

    if hasattr(circuit, "__delitem__"):
        del circuit[position]
        return circuit

    if all(
        hasattr(circuit, name)
        for name in (
            "get_first_node_iter",
            "get_end_node_iter",
            "delete_qnode",
        )
    ):
        end = circuit.get_end_node_iter()
        iterator = circuit.get_first_node_iter()
        length = 0
        while iterator != end:
            length += 1
            iterator = iterator.get_next()

        if position < 0:
            position += length
        if not 0 <= position < length:
            raise IndexError("circuit instruction index out of range")

        iterator = circuit.get_first_node_iter()
        for _ in range(position):
            iterator = iterator.get_next()
        circuit.delete_qnode(iterator)
        return circuit

    length = None
    try:
        length = len(circuit)
    except TypeError:
        for name in ("get_node_num", "get_qprog_size", "size"):
            attribute = getattr(circuit, name, None)
            if attribute is not None:
                length = attribute() if callable(attribute) else attribute
                break

    if length is not None:
        if position < 0:
            position += length
        if not 0 <= position < length:
            raise IndexError("circuit instruction index out of range")
    elif position < 0:
        instructions = list(circuit)
        position += len(instructions)
        if not 0 <= position < len(instructions):
            raise IndexError("circuit instruction index out of range")

    for name in (
        "remove",
        "erase",
        "delete",
        "remove_node",
        "delete_node",
        "remove_gate",
        "delete_qnode",
    ):
        method = getattr(circuit, name, None)
        if callable(method):
            try:
                method(position)
            except TypeError:
                continue
            return circuit

    instructions = list(circuit)
    del instructions[position]
    circuit.clear()
    for instruction in instructions:
        circuit << instruction
    return circuit
