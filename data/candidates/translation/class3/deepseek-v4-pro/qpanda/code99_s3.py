# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit


_UNASSIGNED_TYPE_NAMES = {
    "Variational",
    "Variable",
    "Parameter",
    "var",
    "Var",
}


def _get_parameter_count(gate):
    for name in (
        "get_parameter_count",
        "getParameterCount",
        "getParamCount",
        "get_parameter_number",
        "getParameterNumber",
    ):
        if hasattr(gate, name):
            try:
                value = getattr(gate, name)
                if callable(value):
                    return int(value())
                return int(value)
            except Exception:
                pass
    return 0


def _get_parameter(gate, index):
    for name in ("get_parameter", "getParameter", "getParam"):
        if hasattr(gate, name):
            try:
                return getattr(gate, name)(index)
            except Exception:
                pass
    return None


def _has_unassigned_parameter(gate):
    for i in range(_get_parameter_count(gate)):
        param = _get_parameter(gate, i)
        if param is not None and type(param).__name__ in _UNASSIGNED_TYPE_NAMES:
            return True
    return False


def _iter_circuit_nodes(circuit):
    try:
        yield from list(circuit)
        return
    except TypeError:
        pass

    for count_attr, node_attr in (
        ("get_node_count", "get_node"),
        ("getNodeCount", "getNode"),
        ("get_gate_count", "get_gate"),
        ("getGateCount", "getGate"),
    ):
        if hasattr(circuit, count_attr) and hasattr(circuit, node_attr):
            count = int(getattr(circuit, count_attr)())
            for i in range(count):
                yield getattr(circuit, node_attr)(i)
            return


def remove_unassigned_parameterized_gates(circuit):
    cleaned = QCircuit()

    for node in _iter_circuit_nodes(circuit):
        if (
            hasattr(node, "get_parameter_count")
            or hasattr(node, "getParameterCount")
            or hasattr(node, "getParamCount")
            or hasattr(node, "get_parameter_number")
            or hasattr(node, "getParameterNumber")
        ):
            if _has_unassigned_parameter(node):
                continue

        cleaned << node

    return cleaned
