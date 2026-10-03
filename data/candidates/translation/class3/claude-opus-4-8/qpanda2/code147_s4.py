# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def mcy(qc):
    controls = [qubits[0], qubits[1], qubits[2], qubits[3]]
    target = qubits[4]
    qc << pq.RZ(target, -3.141592653589793 / 2)
    y_gate = pq.Y(target).control(controls)
    qc << y_gate
    qc << pq.RZ(target, 3.141592653589793 / 2)
    return qc


if __name__ == "__main__":
    prog = pq.QProg()
    mcy(prog)
    machine.finalize()
