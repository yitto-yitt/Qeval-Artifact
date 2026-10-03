# EVAL_META: task_id=13, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def custom_rotation_gate():
    try:
        circuit = pq.QCircuit()
        circuit << pq.U3(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)

        program = pq.QProg()
        program << circuit
        machine.directly_run(program)
        return circuit
    finally:
        machine.finalize()
