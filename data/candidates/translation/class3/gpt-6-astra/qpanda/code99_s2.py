# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit):
        return QCircuit(circuit)
    if isinstance(circuit, QProg):
        return QProg(circuit)
    raise TypeError("circuit must be a pyqpanda3 QCircuit or QProg")
