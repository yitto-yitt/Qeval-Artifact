# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq


def create_efficientSU2():
    parameters = None
    for name in ("Parameter", "QParameter", "QParam", "Param", "Symbol"):
        constructor = getattr(pq, name, None)
        if constructor is None:
            continue
        try:
            candidate = [constructor(f"theta[{i}]") for i in range(12)]
            pq.RY(0, candidate[0])
            pq.RZ(0, candidate[0])
        except (TypeError, ValueError, RuntimeError):
            continue
        parameters = candidate
        break

    if parameters is None:
        parameters = [f"theta[{i}]" for i in range(12)]

    circuit = pq.QProg()
    for qubit in range(3):
        circuit << pq.RY(qubit, parameters[qubit])
    for qubit in range(3):
        circuit << pq.RZ(qubit, parameters[3 + qubit])

    circuit << pq.BARRIER([0, 1, 2])
    circuit << pq.CNOT(1, 2)
    circuit << pq.CNOT(0, 1)
    circuit << pq.BARRIER([0, 1, 2])

    for qubit in range(3):
        circuit << pq.RY(qubit, parameters[6 + qubit])
    for qubit in range(3):
        circuit << pq.RZ(qubit, parameters[9 + qubit])

    return circuit
