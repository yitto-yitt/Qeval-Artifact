# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circuit():
    theta = pq.var(0.0)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.RZ(qubits[0], theta)
    return prog, theta


if __name__ == "__main__":
    prog, theta = circuit()
    machine.directly_run(prog)
    print(machine.get_qstate())
    machine.finalize()
