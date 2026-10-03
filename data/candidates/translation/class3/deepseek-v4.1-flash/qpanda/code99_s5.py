# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, Var

try:
    from pyqpanda3.core import Parameter
except ImportError:
    Parameter = Var

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for element in circuit.get_sequence():
        if isinstance(element, QGate):
            params = element.get_parameter()
            if not isinstance(params, (list, tuple)):
                params = [params]
            if any(isinstance(p, (Var, Parameter)) for p in params):
                continue
        new_circuit << element
    return new_circuit
