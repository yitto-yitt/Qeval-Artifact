# EVAL_META: task_id=118, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, H, S

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
atexit.register(lambda: machine.finalize())


def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << H(qubits[3])
    circuit << S(qubits[3]).control(qubits[:3])
    circuit << H(qubits[3])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
