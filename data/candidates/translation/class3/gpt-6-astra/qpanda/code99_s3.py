# EVAL_META: task_id=99, framework=qpanda, class=3
from numbers import Number
from pyqpanda3 import core as pq


def remove_unassigned_parameterized_gates(circuit):
    def read(obj, name):
        value = getattr(obj, name)
        return value() if callable(value) else value

    def nodes(program):
        if hasattr(program, "__iter__"):
            yield from program
            return

        for name in ("get_nodes", "get_node_list", "get_operations"):
            if hasattr(program, name):
                yield from read(program, name)
                return

        if hasattr(program, "get_first_node_iter"):
            iterator = program.get_first_node_iter()
            end = program.get_end_node_iter()
            while iterator != end:
                yield iterator.get_node()
                iterator = iterator.get_next()
            return

        raise TypeError("The circuit does not expose a supported node iterator.")

    def as_operation(node):
        gate_class = getattr(pq, "QGate", None)
        if gate_class is not None and isinstance(node, gate_class):
            return node

        if not hasattr(node, "get_node_type"):
            return node

        kind = str(node.get_node_type()).upper()
        conversions = (
            ("GATE", "cast_qgate", "QGate"),
            ("MEASURE", "cast_qmeasure", "QMeasure"),
            ("RESET", "cast_qreset", "QReset"),
            ("CIRCUIT", "cast_qcircuit", "QCircuit"),
            ("PROG", "cast_qprog", "QProg"),
        )
        for marker, cast_name, class_name in conversions:
            if marker not in kind:
                continue
            cast = getattr(pq, cast_name, None)
            if cast is not None:
                return cast(node)
            cls = getattr(pq, class_name, None)
            if cls is not None:
                return cls(node)
        return node

    def unassigned(value):
        if isinstance(value, Number):
            return False

        for name in ("is_bound", "is_assigned"):
            if hasattr(value, name):
                return not bool(read(value, name))

        for name in ("parameters", "free_symbols"):
            if hasattr(value, name):
                return bool(read(value, name))

        if isinstance(value, (list, tuple)):
            return any(unassigned(item) for item in value)

        if isinstance(value, dict):
            return any(unassigned(item) for item in value.values())

        type_name = type(value).__name__.lower()
        if "parameter" in type_name or "expression" in type_name:
            try:
                float(value)
            except (TypeError, ValueError, RuntimeError):
                return True
        return False

    def has_unassigned_parameters(operation):
        for name in ("is_parameterized", "is_parameterised"):
            if hasattr(operation, name):
                return bool(read(operation, name))

        for name in (
            "get_parameters",
            "get_parameter",
            "get_params",
            "parameters",
            "params",
        ):
            if hasattr(operation, name):
                parameters = read(operation, name)
                if isinstance(parameters, dict):
                    parameters = parameters.values()
                if isinstance(parameters, (str, bytes, Number)):
                    return unassigned(parameters)
                try:
                    return any(unassigned(value) for value in parameters)
                except TypeError:
                    return unassigned(parameters)
        return False

    result = pq.QProg()
    for node in nodes(circuit):
        operation = as_operation(node)
        if not has_unassigned_parameters(operation):
            result << operation
    return result
