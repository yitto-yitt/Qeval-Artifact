# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, QGate, Var

def remove_unassigned_parameterized_gates(circuit):
    new_prog = QProg()
    for node in circuit:
        if isinstance(node, QGate):
            if node.is_parameterized_gate():
                # check all parameters for unassigned Variable
                num_params = node.get_parameter_count()
                skip = False
                for i in range(num_params):
                    param = node.get_parameter(i)
                    if isinstance(param, Var):
                        skip = True
                        break
                if skip:
                    continue   # remove this gate
            # gate has no unassigned parameters → keep it
        # non-gate nodes (if any) are passed through unchanged
        new_prog << node
    return new_prog
