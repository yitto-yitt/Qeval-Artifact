# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits_2 = machine.qAlloc_many(2)
qubits_1 = machine.qAlloc_many(1)

def tensor_circuits():
    top = pq.QCircuit()
    top.insert(pq.X(qubits_1[0]))
    
    bottom = pq.QCircuit()
    bottom.insert(pq.CRY(qubits_2[0], qubits_2[1], 0.2))
    
    tensored = pq.QCircuit()
    tensored.insert(bottom)
    tensored.insert(top)
    
    return tensored

machine.finalize()
