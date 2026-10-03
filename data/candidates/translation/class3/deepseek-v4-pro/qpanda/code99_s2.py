# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

try:
    from pyqpanda3.core import Parameter
except ImportError:
    Parameter = None


def remove_unassigned_parameterized_gates(circuit):
    def _get_gate_count(c):
        for name in ('get_gate_num', 'get_instruction_count', 'get_instruction_num'):
            if hasattr(c, name):
                try:
                    return int(getattr(c, name)())
                except Exception:
                    pass
        try:
            return len(list(circuit))
        except Exception:
            return 0

    def _get_gate(c, index):
        for name in ('get_gate', 'get_instruction'):
            if hasattr(c, name):
                try:
                    return getattr(c, name)(index)
                except Exception:
                    pass
        try:
            return list(circuit)[index]
        except Exception:
            return None

    def _get_param_count(g):
        for name in ('get_parameter_count', 'getParameterCount', 'get_parameter_num'):
            if hasattr(g, name):
                try:
                    return int(getattr(g, name)())
                except Exception:
                    pass
        return 0

    def _get_param(g, index):
        for name in ('get_parameter', 'getParameter'):
            if hasattr(g, name):
                try:
                    return getattr(g, name)(index)
                except Exception:
                    pass
        return None

    def _is_param(p):
        if Parameter is not None:
            return isinstance(p, Parameter)
        return type(p).__name__ in ('Parameter', 'Var')

    new_circuit = QCircuit()
    count = _get_gate_count(circuit)

    for i in range(count):
        gate = _get_gate(circuit, i)
        if gate is None:
            continue

        has_unassigned = False
        pcount = _get_param_count(gate)
        for j in range(pcount):
            if _is_param(_get_param(gate, j)):
                has_unassigned = True
                break

        if has_unassigned:
            continue

        try:
            new_circuit.insert(gate)
        except Exception:
            try:
                new_circuit << gate
            except Exception:
                pass

    return new_circuit
