# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq
import atexit

# Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def inv_circuit(n):
    circuit = pq.QCircuit()
    for i in range(2):
        circuit << pq.H(q[i+1])

    for i in range(2):
        circuit << pq.CNOT(q[i+1], q[i+2+1])
    
    return circuit.dagger()

atexit.register(machine.finalize)
