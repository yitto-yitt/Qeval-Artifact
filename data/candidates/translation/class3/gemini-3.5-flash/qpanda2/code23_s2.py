# EVAL_META: task_id=23, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def dj_constant_oracle():
    circuit = pq.QCircuit()
    circuit << pq.X(qubits[2])
    return circuit

if __name__ == '__main__':
    machine.finalize()
