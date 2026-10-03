# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq


def create_efficientSU2():
    parameter_type = getattr(pq, "Parameter", str)
    parameters = [parameter_type(f"theta[{i}]") for i in range(12)]

    circuit = pq.QCircuit()

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
