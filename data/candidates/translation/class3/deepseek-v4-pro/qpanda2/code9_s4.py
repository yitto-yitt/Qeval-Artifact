# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def create_efficientSU2():
    vqc = pq.VariationalQuantumCircuit()
    thetas = [pq.var(f"theta{i}") for i in range(12)]

    # initial RY layer
    for i in range(3):
        vqc.insert(pq.RY(q[i], thetas[i]))
    vqc.insert(pq.BARRIER(q))

    # initial RZ layer
    for i in range(3):
        vqc.insert(pq.RZ(q[i], thetas[3 + i]))
    vqc.insert(pq.BARRIER(q))

    # full entanglement layer
    vqc.insert(pq.CNOT(q[0], q[1]))
    vqc.insert(pq.CNOT(q[0], q[2]))
    vqc.insert(pq.CNOT(q[1], q[2]))
    vqc.insert(pq.BARRIER(q))

    # final RY layer
    for i in range(3):
        vqc.insert(pq.RY(q[i], thetas[6 + i]))
    vqc.insert(pq.BARRIER(q))

    # final RZ layer
    for i in range(3):
        vqc.insert(pq.RZ(q[i], thetas[9 + i]))

    return vqc


machine.finalize()
