# EVAL_META: task_id=118, framework=qpanda2, class=3
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    try:
        circuit = pq.QCircuit()
        circuit << pq.H(qubits[3])
        circuit << pq.U1(qubits[3], math.pi / 2).control(qubits[:3])
        circuit << pq.H(qubits[3])

        program = pq.QProg()
        program << circuit
        machine.directly_run(program)
        return circuit
    finally:
        machine.finalize()
