# EVAL_META: task_id=99, framework=qpanda, class=3
import numbers
import pyqpanda3.core as pq


def remove_unassigned_parameterized_gates(circuit):
    def unassigned(parameter):
        if isinstance(parameter, numbers.Number):
            return False
        symbols = getattr(parameter, "parameters", None)
        if symbols is not None:
            symbols = symbols() if callable(symbols) else symbols
            if symbols:
                return True
        symbols = getattr(parameter, "free_symbols", None)
        if symbols:
            return True
        for name in ("is_bound", "is_assigned"):
            predicate = getattr(parameter, name, None)
            if predicate is not None:
                return not bool(predicate() if callable(predicate) else predicate)
        try:
            complex(parameter)
            return False
        except (TypeError, ValueError, RuntimeError):
            return True

    def parameters(gate):
        for name in ("get_params", "get_parameters", "get_parameter", "params"):
            member = getattr(gate, name, None)
            if member is None:
                continue
            value = member() if callable(member) else member
            if value is None:
                return ()
            if isinstance(value, (str, bytes, numbers.Number)):
                return (value,)
            try:
                return tuple(value)
            except TypeError:
                return (value,)
        return ()

    def unwrap(node):
        member = getattr(node, "get_node", None)
        if member is not None:
            node = member()
        type_member = getattr(node, "get_node_type", None)
        if type_member is None:
            return node
        node_type = type_member()
        enums = [
            getattr(pq, name, None)
            for name in ("NodeType", "QNodeType")
        ]
        wrappers = (
            ("GATE_NODE", "QGate"),
            ("CIRCUIT_NODE", "QCircuit"),
            ("PROG_NODE", "QProg"),
            ("MEASURE_GATE", "QMeasure"),
            ("RESET_NODE", "QReset"),
        )
        for label, class_name in wrappers:
            matches = label in str(node_type)
            for enum in enums:
                if enum is not None and hasattr(enum, label):
                    matches = matches or node_type == getattr(enum, label)
            cls = getattr(pq, class_name, None)
            if matches and cls is not None:
                if isinstance(node, cls):
                    return node
                return cls(node)
        return node

    def nodes(container):
        first = getattr(container, "get_first_node_iter", None)
        end = getattr(container, "get_end_node_iter", None)
        if first is not None and end is not None:
            iterator, sentinel = first(), end()
            while iterator != sentinel:
                yield unwrap(iterator)
                advance = getattr(iterator, "get_next", None)
                iterator = advance() if advance is not None else next(iterator)
            return
        for node in container:
            yield unwrap(node)

    def filtered(container):
        result = type(container)()
        circuit_class = getattr(pq, "QCircuit", None)
        program_class = getattr(pq, "QProg", None)
        container_classes = tuple(
            cls for cls in (circuit_class, program_class) if cls is not None
        )
        for node in nodes(container):
            if isinstance(node, container_classes):
                result << filtered(node)
            elif not any(unassigned(parameter) for parameter in parameters(node)):
                result << node

        if circuit_class is not None and isinstance(container, circuit_class):
            get_dagger = getattr(container, "is_dagger", None)
            set_dagger = getattr(result, "set_dagger", None)
            if get_dagger is not None and set_dagger is not None:
                set_dagger(get_dagger())

            get_controls = getattr(container, "get_control_qubits", None)
            set_controls = getattr(result, "set_control", None)
            if get_controls is not None and set_controls is not None:
                try:
                    controls = get_controls()
                except TypeError:
                    vector_class = getattr(pq, "QVec", list)
                    controls = vector_class()
                    get_controls(controls)
                if controls:
                    set_controls(controls)
        return result

    return filtered(circuit)
