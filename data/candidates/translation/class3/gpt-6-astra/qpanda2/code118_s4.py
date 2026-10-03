# EVAL_META: task_id=118, framework=qpanda2, class=3
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_c3sx_circuit():
    program = pq.QProg()
    program << pq.RX(qubits[3], math.pi / 2).control(qubits[:3])
    program << pq.U1(qubits[2], math.pi / 4).control(qubits[:2])
    machine.directly_run(program)
    return program


if __name__ == "__main__":
    try:
        create_c3sx_circuit()
    finally:
        machine.finalize()
