# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, X, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_custom_controlled():
    controls = [qubits[0], qubits[3]]
    circuit = QCircuit()
    circuit << X(qubits[1]).control(controls)
    circuit << H(qubits[2]).control(controls)

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
