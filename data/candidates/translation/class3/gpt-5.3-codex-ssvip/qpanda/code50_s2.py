# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit
    if hasattr(circuit, "ops"):
        del circuit.ops[position]
        return circuit
    if isinstance(circuit, QCircuit) and hasattr(circuit, "__dict__"):
        for k in ("data", "ops", "_ops", "_gates"):
            if k in circuit.__dict__ and isinstance(circuit.__dict__[k], list):
                del circuit.__dict__[k][position]
                return circuit
    raise AttributeError("Unsupported circuit object: cannot locate mutable gate sequence.")
