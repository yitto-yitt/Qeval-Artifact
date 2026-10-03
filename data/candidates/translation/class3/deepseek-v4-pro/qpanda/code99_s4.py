# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *
import numbers

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = type(circuit)()
    for node in circuit:
        if isinstance(node, QGate):
            params = []
            try:
                param = node.get_parameter()
                if isinstance(param, (list, tuple)):
                    params = list(param)
                else:
                    params = [param]
            except AttributeError:
                try:
                    angle = node.get_angle()
                    params = [angle]
                except AttributeError:
                    params = []
            has_unassigned = False
            for p in params:
                if not isinstance(p, numbers.Number):
                    has_unassigned = True
                    break
            if has_unassigned:
                continue
        new_circuit << node
    return new_circuit
