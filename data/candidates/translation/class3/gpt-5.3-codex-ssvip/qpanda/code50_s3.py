# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit
    if hasattr(circuit, "m_circuit"):
        del circuit.m_circuit[position]
        return circuit
    if isinstance(circuit, (list, tuple)):
        if isinstance(circuit, tuple):
            lst = list(circuit)
            del lst[position]
            return tuple(lst)
        del circuit[position]
        return circuit
    raise TypeError("Unsupported circuit type for gate removal.")
