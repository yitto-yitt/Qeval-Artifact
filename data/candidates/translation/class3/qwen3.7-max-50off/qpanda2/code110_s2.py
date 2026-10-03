# EVAL_META: task_id=110, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    for _ in range(n):
        qc = pq.QCircuit()
        qc.insert(circuit)
        qc_list.append(qc)
    return qc_list

machine.finalize()
