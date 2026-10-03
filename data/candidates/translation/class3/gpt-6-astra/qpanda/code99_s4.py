# EVAL_META: task_id=99, framework=qpanda, class=3
import numbers
from pyqpanda3 import core


def remove_unassigned_parameterized_gates(circuit):
    def read_attribute(obj, name):
        value = getattr(obj, name)
        return value() if callable(value) else value

    def iter_nodes(program):
        if hasattr(program, "__iter__"):
            yield from program
            return

        if hasattr(program, "get_first_node_iter"):
            iterator = program.get_first_node_iter()
            end = program.get_end_node_iter()
            while iterator != end:
                yield iterator.get_node()
                iterator = iterator.get_next()
            return

        for name in ("get_node_list", "get_nodes", "get_all_nodes"):
            if hasattr(program, name):
                yield from read_attribute(program, name)
                return

        if hasattr(program, "__len__") and hasattr(program, "__getitem__"):
            for index in range(len(program)):
                yield program[index]
            return

        raise TypeError("The circuit does not expose a supported node interface.")

    def as_gate(node):
        gate_class = getattr(core, "QGate", None)
        if gate_class is None:
            return None
        if isinstance(node, gate_class):
            return node

        if hasattr(node, "get_node_type"):
            node_type = node.get_node_type()
            node_types = getattr(core, "NodeType", None)
            gate_type = getattr(node_types, "GATE_NODE", None)
            if gate_type is not None and node_type != gate_type:
                return None

        try:
            return gate_class(node)
        except (TypeError, ValueError, RuntimeError):
            return None

    def is_unassigned(value):
        if isinstance(value, (numbers.Number, str, bytes)):
            return False

        for name in ("parameters", "free_symbols"):
            if hasattr(value, name):
                return bool(read_attribute(value, name))

        for name in ("is_bound", "is_assigned"):
            if hasattr(value, name):
                return not bool(read_attribute(value, name))

        parameter_class = getattr(core, "Parameter", None)
        if parameter_class is not None and isinstance(value, parameter_class):
            try:
                float(value)
            except (TypeError, ValueError, RuntimeError):
                return True

        return False

    def has_unassigned_parameter(gate):
        if hasattr(gate, "is_parameterized"):
            return bool(read_attribute(gate, "is_parameterized"))

        for name in ("params", "get_parameters", "get_parameter", "parameters"):
            if not hasattr(gate, name):
                continue
            parameters = read_attribute(gate, name)
            if is_unassigned(parameters):
                return True
            if parameters is None or isinstance(parameters, numbers.Number):
                return False
            try:
                return any(is_unassigned(parameter) for parameter in parameters)
            except TypeError:
                return is_unassigned(parameters)
        return False

    circuit_class = getattr(core, "QCircuit", None)
    if circuit_class is not None and isinstance(circuit, circuit_class):
        result = circuit_class()
    else:
        result = core.QProg()

    for node in iter_nodes(circuit):
        if hasattr(node, "get_node") and not hasattr(node, "get_node_type"):
            node = node.get_node()

        gate = as_gate(node)
        if gate is not None and has_unassigned_parameter(gate):
            continue

        if gate is not None:
            result << gate
            continue

        try:
            result << node
        except TypeError:
            for name in ("QMeasure", "QReset", "QCircuit", "QProg"):
                node_class = getattr(core, name, None)
                if node_class is None:
                    continue
                try:
                    converted = node_class(node)
                    result << converted
                    break
                except (TypeError, ValueError, RuntimeError):
                    continue
            else:
                raise TypeError("The circuit contains an unsupported node.")

    return result
