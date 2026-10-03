# EVAL_META: task_id=69, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, H, S

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << S(qubits[1]).control([qubits[0]])
    circuit << H(qubits[1])
    circuit << S(qubits[0]).dagger().control([qubits[1]])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
