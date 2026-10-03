# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = type(circuit)()
    for gate in circuit.get_ops():
        try:
            params = gate.get_params()
        except AttributeError:
            params = []
        has_unassigned = False
        for p in params:
            if isinstance(p, Parameter) and not p.is_assigned():
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit << gate
    return new_circuit
