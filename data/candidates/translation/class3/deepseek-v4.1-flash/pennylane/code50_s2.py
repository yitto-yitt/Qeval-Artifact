# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript


def remove_gate_in_position(circuit, position):
    ops = list(circuit.operations)
    ops.pop(position)
    return QuantumScript(ops=ops, measurements=list(circuit.measurements), shots=circuit.shots)
