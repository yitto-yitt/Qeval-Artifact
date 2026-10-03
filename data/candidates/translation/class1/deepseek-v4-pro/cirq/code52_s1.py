# EVAL_META: task_id=52, framework=cirq, class=1
import cirq


def send_bits(bitstring):
    q_sender = cirq.NamedQubit('sender')
    q_receiver = cirq.NamedQubit('receiver')
    circuit = cirq.Circuit()

    # Step 1: prepare entanglement
    circuit.append([cirq.H(q_sender)])
    circuit.append([cirq.CNOT(q_sender, q_receiver)])

    # Step 2: encode the two classical bits
    if bitstring[1] == "1":
        circuit.append([cirq.Z(q_sender)])
    if bitstring[0] == "1":
        circuit.append([cirq.X(q_sender)])

    # Step 3: Bell measurement on the sender's side
    circuit.append([cirq.CNOT(q_sender, q_receiver)])
    circuit.append([cirq.H(q_sender)])
    circuit.append([cirq.measure(q_sender, key='m0'),
                    cirq.measure(q_receiver, key='m1')])

    return circuit
