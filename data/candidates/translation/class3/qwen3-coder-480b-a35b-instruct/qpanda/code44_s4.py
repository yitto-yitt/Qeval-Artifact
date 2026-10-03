# EVAL_META: task_id=44, framework=qpanda, class=3
import pyqpanda3.core as pq

def tensor_circuits():
    machine = pq.QMachine()
    qubits_1 = machine.qAlloc_many(1)
    qubits_2 = machine.qAlloc_many(2)
    
    top = pq.QCircuit()
    top.insert(pq.X(qubits_1[0]))
    
    bottom = pq.QCircuit()
    bottom.insert(pq.CRY(qubits_2[0], qubits_2[1], 0.2))
    
    tensored = bottom + top
    return tensored
