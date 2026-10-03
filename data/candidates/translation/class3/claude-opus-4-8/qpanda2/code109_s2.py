# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    theta = pq.var(0.0)
    prog = pq.QProg()
    vqc = pq.VariationalQuantumCircuit()
    vqc.insert(pq.VariationalQuantumGate_H(qubits[0]))
    vqc.insert(pq.VariationalQuantumGate_RZ(qubits[0], theta))
    return vqc

if __name__ == "__main__":
    vqc = circuit()
    prog = pq.QProg()
    prog.insert(vqc.feed())
    result = machine.prob_run_dict(prog, qubits)
    print(result)
    machine.finalize()
