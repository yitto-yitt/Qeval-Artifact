# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM, CNOT

def create_swap_gate():
    circuit = QCircuit()
    circuit << CNOT(0, 1) << CNOT(1, 0) << CNOT(0, 1)
    program = QProg()
    program << circuit
    simulator = CPUQVM()
    simulator.run(program, 1)
    return circuit
