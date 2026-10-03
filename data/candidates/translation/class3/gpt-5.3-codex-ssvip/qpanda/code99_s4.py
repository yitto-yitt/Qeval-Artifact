# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    circuit_without_params = QCircuit()
    if not hasattr(circuit, "data"):
        return circuit_without_params

    circuit_data = list(circuit.data)
    for instruction in circuit_data:
        op = None
        qargs = []
        cargs = []

        if isinstance(instruction, dict):
            op = instruction.get("operation", instruction.get("op", None))
            qargs = instruction.get("qubits", instruction.get("qargs", []))
            cargs = instruction.get("clbits", instruction.get("cargs", []))
        elif isinstance(instruction, (list, tuple)):
            if len(instruction) >= 3:
                op, qargs, cargs = instruction[0], instruction[1], instruction[2]
            elif len(instruction) == 2:
                op, qargs = instruction[0], instruction[1]
                cargs = []
            elif len(instruction) == 1:
                op = instruction[0]
        else:
            op = getattr(instruction, "operation", getattr(instruction, "op", None))
            qargs = getattr(instruction, "qubits", getattr(instruction, "qargs", []))
            cargs = getattr(instruction, "clbits", getattr(instruction, "cargs", []))

        params = getattr(op, "params", None)
        has_unassigned = False
        if params is not None:
            if not isinstance(params, (list, tuple)):
                name = type(params).__name__.lower()
                has_unassigned = ("param" in name) and ("value" not in name)
            elif len(params) > 0:
                p0 = params[0]
                name = type(p0).__name__.lower()
                has_unassigned = ("param" in name) and ("value" not in name)

        if not has_unassigned and op is not None:
            try:
                circuit_without_params.insert(op, qargs, cargs)
            except Exception:
                try:
                    circuit_without_params << op
                except Exception:
                    pass

    return circuit_without_params
