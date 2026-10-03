# EVAL_META: task_id=81, framework=qpanda2, class=3
import pyqpanda as pq
import tempfile
import os
import atexit

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

# Manual Cleanup
atexit.register(machine.finalize)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    
    # Write the QASM string to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.qasm') as f:
        f.write(qasm_string)
        temp_file_path = f.name
        
    try:
        prog = pq.convert_qasm_to_qprog(temp_file_path, machine)
    finally:
        os.remove(temp_file_path)
        
    return prog
