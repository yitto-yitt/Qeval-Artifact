# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Parameter

def remove_unassigned_parameterized_gates(circuit):
    def _is_parameter(obj):
        if isinstance(obj, Parameter):
            return True
        if type(obj).__name__ in ("Parameter", "ParameterVector", "Var"):
            return True
        if hasattr(obj, "is_parameter") and obj.is_parameter():
            return True
        return False

    def _has_unassigned_parameter(gate):
        if hasattr(gate, "is_parameterized"):
            try:
                if gate.is_parameterized():
                    return True
            except Exception:
                pass
        for attr in ("get_params", "params", "get_param", "param", "parameters"):
            if hasattr(gate, attr):
                val = getattr(gate, attr)
                if callable(val):
                    try:
                        val = val()
                    except Exception:
                        continue
                if isinstance(val, (list, tuple, set)):
                    if any(_is_parameter(p) for p in val):
                        return True
                else:
                    if _is_parameter(val):
                        return True
        if _is_parameter(gate):
            return True
        return False

    def _iter_gates(circ):
        for meth in ("get_sequence", "get_instructions", "instructions", "get_gates", "get_qgate_sequence"):
            if hasattr(circ, meth):
                seq = getattr(circ, meth)
                try:
                    seq = seq() if callable(seq) else seq
                    return list(seq)
                except Exception:
                    pass
        try:
            return list(circ)
        except Exception:
            pass
        return []

    new_circuit = QCircuit()
    for gate in _iter_gates(circuit):
        if not _has_unassigned_parameter(gate):
            new_circuit << gate
    return new_circuit
