# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    sender = cirq.LineQubit(0)
    receiver = cirq.LineQubit(1)
    circuit = cirq.Circuit()
    
    # Create Bell pair
    circuit.append(cirq.H(sender))
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.Moment(cirq.GlobalPhaseGate(1)))
    
    # Apply corrections based on bitstring
    if bitstring[1] == "1":
        circuit.append(cirq.Z(sender))
    if bitstring[0] == "1":
        circuit.append(cirq.X(sender))
    
    circuit.append(cirq.Moment(cirq.GlobalPhaseGate(1)))
    
    # Perform Bell measurement
    circuit.append(cirq.CNOT(sender, receiver))
    circuit.append(cirq.H(sender))
    
    # Measure both qubits
    circuit.append(cirq.measure(sender, key='sender'))
    circuit.append(cirq.measure(receiver, key='receiver'))
    
    return circuit
