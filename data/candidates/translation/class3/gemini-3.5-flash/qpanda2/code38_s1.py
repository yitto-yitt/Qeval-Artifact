# EVAL_META: task_id=38, framework=qpanda2, class=3
import pyqpanda as pq

# Initialize global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = pq.QCircuit()
    circuit << pq.H(q[0])
    circuit << pq.CRZ(q[0], q[1], theta)
    circuit << pq.H(q[1])
    circuit << pq.CRY(q[1], q[0], theta)
    return circuit

machine.finalize()
