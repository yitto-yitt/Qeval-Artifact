# EVAL_META: task_id=99, framework=pennylane, class=3
import sympy
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    def is_symbolic(p):
        if isinstance(p, sympy.Basic):
            return True
        if isinstance(p, str):
            return True
        if hasattr(p, "__iter__") and not isinstance(p, (str, bytes)):
            try:
                return any(is_symbolic(sub_p) for sub_p in p)
            except Exception:
                pass
        return False

    new_ops = []
    for op in circuit.operations:
        if not any(is_symbolic(p) for p in op.data):
            new_ops.append(op)
            
    return qml.tape.QuantumScript(new_ops, circuit.measurements, circuit.prep)
