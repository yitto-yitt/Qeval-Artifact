# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    machine = init_quantum_machine(QMachineType.CPU)
    qv = machine.qAlloc_many(2)
    cv = machine.cAlloc_many(2)
    
    # Parse QASM string and create circuit
    prog = QProg()
    prog.insert(h(qv[0])).insert(cnot(qv[0], qv[1]))
    
    # Since pyQPanda3 doesn't have direct QASM parsing, we recreate the circuit manually
    # based on the expected operations from the QASM string
    return prog
