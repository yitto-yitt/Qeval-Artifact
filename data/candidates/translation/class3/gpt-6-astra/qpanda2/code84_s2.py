# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, U3

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def controlled_custom_unitary_circuit():
    try:
        circuit = QProg()
        circuit << U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]])
        machine.directly_run(circuit)
        return circuit
    finally:
        machine.finalize()
