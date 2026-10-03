# EVAL_META: task_id=49, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def simple_elitzur_vaidman():
    try:
        circuit = QCircuit()
        circuit << H(qubits[0])
        circuit << CNOT(qubits[0], qubits[1])
        circuit << H(qubits[0])

        program = QProg()
        program << circuit
        machine.directly_run(program)
        return circuit
    finally:
        machine.finalize()
