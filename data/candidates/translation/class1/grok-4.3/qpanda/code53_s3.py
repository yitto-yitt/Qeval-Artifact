# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    circuit = pq.QCircuit()
    for i in range(8):
        if (a >> i) & 1:
            circuit.insert(pq.X(q[i]))
        if (b >> i) & 1:
            circuit.insert(pq.X(q[i]))
    circuit.insert(pq.measure_all(q, c))
    prog = pq.QProg()
    prog.insert(circuit)
    result = machine.run_with_configuration(prog, c, shots=1024)
    total = sum(result.values())
    dist = {}
    for k, v in result.items():
        bin_str = format(k, '08b')
        dist[bin_str] = v / total
    return dist
