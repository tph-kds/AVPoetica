if __name__ == "__main__":
    import os
    os.environ["PYTEST_ADDOPTS"] = "--ignore=tests/test_delete_json.py"

    import re
    import json

    response = """```json
    {
    "responses": [
        {"message": "Hello"},
        {"message": "World"}
    ]
    }```"""

    # Strip markdown code block markers
    if response.startswith("```"):
        match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            try:
                response = json.loads(json_str)
                print(response)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)