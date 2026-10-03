# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CNOT, T, QCircuit, QProg, CPUQVM


def initialize_cnot_dihedral():
    circuit = QCircuit()
    circuit << CNOT(0, 1) << T(0)

    program = QProg()
    program << circuit

    simulator = CPUQVM()
    simulator.run(program, 1)
    return circuit
