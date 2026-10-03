# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QGate

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = type(circuit)()
    nodes = circuit.get_sequences() if hasattr(circuit, 'get_sequences') else list(circuit)
    for node in nodes:
        if isinstance(node, QGate) and node.is_parameterized():
            continue
        new_circuit << node
    return new_circuit
