# EVAL_META: task_id=10, framework=qpanda2, class=3
from math import pi
from pyqpanda import CPUQVM, QCircuit, QProg, U3

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_operator():
    try:
        circuit = QCircuit()
        circuit << U3(qubits[0], pi, 0.0, pi)
        circuit << U3(qubits[1], pi, 0.0, pi)
        program = QProg()
        program << circuit
        machine.directly_run(program)
        return circuit
    finally:
        machine.finalize()
