# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit


def remove_gate_in_position(circuit, position):
    try:
        circuit.erase(position)
    except AttributeError:
        try:
            del circuit[position]
        except (TypeError, AttributeError):
            gates = list(circuit)
            circuit.clear()
            for idx, gate in enumerate(gates):
                if idx != position:
                    circuit << gate
    return circuit
