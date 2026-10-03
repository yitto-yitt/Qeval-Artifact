# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    # In PennyLane, we can create a template that represents the circuit
    # by defining a function that applies the operations from the circuit
    def gate_template(params=None, wires=None):
        # Apply the operations from the circuit
        for op in circ.operations:
            if hasattr(op, 'parameters') and len(op.parameters) > 0:
                getattr(qml, op.name)(*op.parameters, wires=op.wires.tolist())
            else:
                getattr(qml, op.name)(wires=op.wires.tolist())
    
    return gate_template
