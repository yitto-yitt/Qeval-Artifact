# EVAL_META: task_id=60, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, S, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(lambda: machine.finalize())


def create_cy_gate():
    circuit = QCircuit()
    circuit << S(qubits[1]).dagger()
    circuit << CNOT(qubits[0], qubits[1])
    circuit << S(qubits[1])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
