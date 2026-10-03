# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

class Parameter:
    """Symbolic unassigned parameter placeholder."""
    pass

def remove_unassigned_parameterized_gates(circuit):
    # circuit is a QuantumTape
    new_ops = []
    for op in circuit.operations:
        if not any(isinstance(p, Parameter) for p in op.parameters):
            new_ops.append(op)
    # preserve state preparations if any
    prep = getattr(circuit, '_prep', [])
    new_tape = qml.tape.QuantumTape(new_ops, circuit.measurements, prep=prep)
    return new_tape
