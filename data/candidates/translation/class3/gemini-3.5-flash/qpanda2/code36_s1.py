# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def bv_function(s):
    n = len(s)
    circuit = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << pq.CNOT(qubits[index], qubits[n])
    return circuit

machine.finalize()
