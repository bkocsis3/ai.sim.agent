from cal.tools.math_tools import add_numbers, sub_numbers

def test_subtraction_tool_call(agent):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "Subtract 10 from 3"}
        ],
        "tools": [add_numbers, sub_numbers],
        "tool_choice": "auto"
    })

    tool_msg = None
    for msg in response["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_msg = msg
            break

    assert tool_msg is not None, "Agent did not call any tool"

    tool_call = tool_msg.tool_calls[0]
    assert tool_call["function"]["name"] == "sub_numbers"
    assert tool_call["function"]["arguments"] == '{"a":10,"b":3}'
