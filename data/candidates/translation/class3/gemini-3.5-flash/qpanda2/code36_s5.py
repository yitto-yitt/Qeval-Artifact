# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def bv_function(s):
    n = len(s)
    qubits = [global_qubits[i] for i in range(n + 1)]
    circuit = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << pq.CNOT(qubits[index], qubits[n])
    return circuit

machine.finalize()
