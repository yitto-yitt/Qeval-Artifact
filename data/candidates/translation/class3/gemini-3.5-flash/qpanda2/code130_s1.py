# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def inv_circuit(n):
    qubits = [global_qubits[i] for i in range(n)]
    circuit = pq.QCircuit()
    
    for i in range(2):
        circuit << pq.H(qubits[i+1])
        
    for i in range(2):
        circuit << pq.CNOT(qubits[i+1], qubits[i+3])
        
    return circuit.dagger()

machine.finalize()
