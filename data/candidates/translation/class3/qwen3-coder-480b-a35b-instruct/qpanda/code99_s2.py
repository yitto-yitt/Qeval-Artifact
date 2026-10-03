# EVAL_META: task_id=99, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.extensions import *

def remove_unassigned_parameterized_gates(circuit):
    # Get the number of qubits and classical bits
    qubit_num = len(circuit.get_allocated_qubits())
    cbit_num = len(circuit.get_allocated_cbits())
    
    # Create a new quantum program without unassigned parameterized gates
    new_prog = QProg()
    new_circuit = QCircuit()
    
    # Extract all gates from the original circuit
    gates = []
    for gate in circuit.get_gates():
        gates.append(gate)
    
    for gate in gates:
        # Check if the gate has unassigned parameters
        # For parameterized gates, we need to check if they have free parameters
        param_count = gate.get_parameter_count()
        has_unassigned_param = False
        
        for i in range(param_count):
            param = gate.get_parameter(i)
            # If parameter is not bound (not a constant), it's unassigned
            if hasattr(param, 'is_symbolic') and param.is_symbolic():
                has_unassigned_param = True
                break
            elif hasattr(param, '__class__') and 'Parameter' in str(type(param)):
                has_unassigned_param = True
                break
                
        # Only add gates without unassigned parameters
        if not has_unassigned_param:
            new_circuit.insert(gate)
    
    new_prog.insert(new_circuit)
    
    # Create a new circuit based on the processed program
    # We need to build a new circuit with proper qubit allocation
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(qubit_num)
    cbits = qvm.cAlloc_many(cbit_num) if cbit_num > 0 else []
    
    # Create a new circuit and add the processed gates
    result_circuit = QCircuit()
    temp_prog = QProg()
    temp_prog.insert(new_circuit)
    
    # Since we can't directly create an empty circuit and append like Qiskit,
    # we'll return the program containing the filtered circuit
    qvm.finalize()
    
    return new_circuit
