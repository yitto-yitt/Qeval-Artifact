# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    circuit_without_params = QCircuit()
    for gate in circuit:
        params = None
        if hasattr(gate, "get_parameters"):
            try:
                params = gate.get_parameters()
            except Exception:
                params = None
        elif hasattr(gate, "params"):
            params = gate.params

        has_unassigned = False
        if params is not None:
            if isinstance(params, (list, tuple)):
                for p in params:
                    if p is None:
                        has_unassigned = True
                        break
                    if hasattr(p, "is_bound"):
                        try:
                            if not p.is_bound():
                                has_unassigned = True
                                break
                        except Exception:
                            pass
                    if hasattr(p, "name") and not isinstance(p, (int, float, complex)):
                        has_unassigned = True
                        break
            else:
                p = params
                if p is None:
                    has_unassigned = True
                elif hasattr(p, "is_bound"):
                    try:
                        if not p.is_bound():
                            has_unassigned = True
                    except Exception:
                        pass
                elif hasattr(p, "name") and not isinstance(p, (int, float, complex)):
                    has_unassigned = True

        if not has_unassigned:
            circuit_without_params.insert(gate)
    return circuit_without_params
