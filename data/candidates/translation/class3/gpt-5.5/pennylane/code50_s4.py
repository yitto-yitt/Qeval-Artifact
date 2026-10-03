# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "operations"):
        try:
            del circuit.operations[position]
            return circuit
        except (TypeError, AttributeError):
            ops = list(circuit.operations)
            del ops[position]
            measurements = list(getattr(circuit, "measurements", []))
            if hasattr(circuit, "_ops"):
                circuit._ops = ops
                return circuit
            try:
                return circuit.copy(operations=ops)
            except Exception:
                return qml.tape.QuantumScript(ops, measurements, shots=getattr(circuit, "shots", None))

    if hasattr(circuit, "_ops"):
        del circuit._ops[position]
        return circuit

    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit

    del circuit[position]
    return circuit
