# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    if circuit is None:
        return QCircuit()

    new_circuit = QCircuit()

    gate_list = []
    if hasattr(circuit, "get_qgate_list"):
        gate_list = circuit.get_qgate_list()
    elif hasattr(circuit, "get_gate_list"):
        gate_list = circuit.get_gate_list()
    elif hasattr(circuit, "gates"):
        gate_list = list(circuit.gates)
    else:
        try:
            gate_list = list(circuit)
        except Exception:
            gate_list = []

    for gate in gate_list:
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
                    if isinstance(p, str):
                        has_unassigned = True
                        break
                    if hasattr(p, "is_parameter") and bool(getattr(p, "is_parameter")):
                        has_unassigned = True
                        break
                    if hasattr(p, "name") and not isinstance(p, (int, float, complex, bool)):
                        try:
                            float(p)
                        except Exception:
                            has_unassigned = True
                            break
            else:
                p = params
                if p is None or isinstance(p, str):
                    has_unassigned = True
                elif hasattr(p, "is_parameter") and bool(getattr(p, "is_parameter")):
                    has_unassigned = True
                elif hasattr(p, "name") and not isinstance(p, (int, float, complex, bool)):
                    try:
                        float(p)
                    except Exception:
                        has_unassigned = True

        if not has_unassigned:
            new_circuit << gate

    return new_circuit
