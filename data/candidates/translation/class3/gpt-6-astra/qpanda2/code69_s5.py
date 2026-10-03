# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, S

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    program = QProg()
    program << H(qubits[0])
    program << S(qubits[1]).control([qubits[0]])
    program << H(qubits[1])
    program << S(qubits[0]).dagger().control([qubits[1]])
    machine.directly_run(program)
    return program


if __name__ == "__main__":
    try:
        create_quantum_circuit_based_h0_cs01_h1_csdg10()
    finally:
        machine.finalize()
