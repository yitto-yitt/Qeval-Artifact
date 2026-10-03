# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_swap_gate():
    try:
        circuit = QCircuit()
        circuit << CNOT(qubits[0], qubits[1])
        circuit << CNOT(qubits[1], qubits[0])
        circuit << CNOT(qubits[0], qubits[1])

        program = QProg()
        program << circuit
        machine.directly_run(program)
        return circuit
    finally:
        machine.finalize()
