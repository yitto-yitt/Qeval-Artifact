# EVAL_META: task_id=130, framework=qpanda, class=3
import pyqpanda3.core as pq

def inv_circuit(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    
    circuit = pq.QCircuit()
    for i in range(2):
        circuit << pq.H(q[i+1])

    for i in range(2):
        circuit << pq.CNOT(q[i+1], q[i+3])
    
    return circuit.dagger()
