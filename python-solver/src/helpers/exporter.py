from ortools.sat.python import cp_model
from google.protobuf import text_format

def export_cp_model(model, filename, text_format_output=True):
    # Convert CP model to protocol buffer
    model_proto = model.Proto()

    if text_format_output:
        # Export as .pbtxt (human-readable)
        with open(f"{filename}.pbtxt", "w") as f:
            f.write(text_format.MessageToString(model_proto))
        print(f"Exported model to {filename}.pbtxt")
    else:
        # Export as .pb (binary protobuf)
        with open(f"{filename}.pb", "wb") as f:
            f.write(model_proto.SerializeToString())
        print(f"Exported model to {filename}.pb")
