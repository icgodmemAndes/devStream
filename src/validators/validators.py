from jsonschema import validate
import traceback
import jsonschema

from src.errors.errors import BadRequest

CreateBlacklistSchema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minimum": 6, "maximum": 64, "format": "email"},
        "appUuid":  {"type": "string", "pattern": r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"},
        "blockedReason":  {"type": "string", "minimum": 3, "maximum": 255}
    },
    "required": ["email", "appUuid"]
}


def validate_schema(data, schema):
    try:
        # Validate against JSON Schema
        validate(instance=data, schema=schema)

        return None  # No errors
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest


