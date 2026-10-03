# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    top = pq.QCircuit()
    top.insert(pq.X(qubits[0]))
    
    bottom = pq.QCircuit()
    bottom.insert(pq.CRY(qubits[1], qubits[2], 0.2))
    
    tensored = pq.QCircuit()
    tensored.insert(bottom)
    tensored.insert(top)
    
    return tensored

machine.finalize()
