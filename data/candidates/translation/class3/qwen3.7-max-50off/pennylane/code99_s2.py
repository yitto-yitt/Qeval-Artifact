# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import sympy

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        unassigned = False
        for p in op.parameters:
            if isinstance(p, (str, sympy.Basic)):
                unassigned = True
                break
            if isinstance(p, (list, tuple)):
                if any(isinstance(x, (str, sympy.Basic)) for x in p):
                    unassigned = True
                    break
        if not unassigned:
            new_ops.append(op)
            
    return qml.tape.QuantumTape(new_ops, circuit.measurements)
