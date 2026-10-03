# EVAL_META: task_id=99, framework=qpanda, class=3
import pyqpanda3.core as pq


def remove_unassigned_parameterized_gates(circuit):
    result = type(circuit)(circuit)

    def first_method(obj, names):
        for name in names:
            method = getattr(obj, name, None)
            if callable(method):
                return method
        return None

    def is_unassigned(value):
        parameter_type = getattr(pq, "Parameter", None)
        if isinstance(parameter_type, type) and isinstance(value, parameter_type):
            return True
        return type(value).__name__ == "Parameter"

    def should_remove(node):
        gate = node
        getter = first_method(node, ("get_qgate", "get_gate"))
        if getter is not None:
            try:
                gate = getter()
            except (TypeError, RuntimeError, ValueError):
                return False
        elif not isinstance(node, pq.QGate):
            try:
                gate = pq.QGate(node)
            except (TypeError, RuntimeError, ValueError):
                return False

        getter = first_method(
            gate,
            ("get_parameters", "get_parameter", "get_gate_parameter", "get_params"),
        )
        if getter is not None:
            params = getter()
        else:
            params = getattr(gate, "params", ())

        if is_unassigned(params):
            return True
        try:
            return len(params) > 0 and is_unassigned(params[0])
        except (TypeError, IndexError):
            return False

    begin = first_method(result, ("get_first_node", "begin"))
    end = first_method(result, ("get_end_node", "end"))
    erase = first_method(result, ("delete_qnode", "erase", "remove_node"))

    if begin is not None and end is not None and erase is not None:
        iterator = begin()
        sentinel = end()
        while iterator != sentinel:
            next_iterator = iterator.get_next()
            get_node = getattr(iterator, "get_node", None)
            node = get_node() if callable(get_node) else iterator
            if should_remove(node):
                erase(iterator)
            iterator = next_iterator
        return result

    try:
        nodes = iter(circuit)
    except TypeError:
        # Native numeric-only circuit representations cannot contain an
        # unassigned symbolic gate parameter.
        return result

    result = type(circuit)()
    for node in nodes:
        if not should_remove(node):
            result << node
    return result
