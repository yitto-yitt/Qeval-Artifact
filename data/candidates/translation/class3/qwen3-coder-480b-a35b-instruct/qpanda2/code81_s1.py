# EVAL_META: task_id=81, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(2)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    prog = pq.QProg()
    prog.insert(pyqpanda.QProg.from_qasm_str(qasm_string))
    return prog

machine.finalize()
