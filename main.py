from fastmcp import FastMCP
from typing import List
import boto3
from botocore.exceptions import ClientError


# ============================================================
# DynamoDB Configuration
# ============================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

table = dynamodb.Table("EmployeeLeaves")


# ============================================================
# Create MCP Server
# ============================================================

mcp = FastMCP("LeaveManager")


# ============================================================
# Tool 1: Check Leave Balance
# ============================================================

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee."""

    response = table.get_item(
        Key={
            "employee_id": employee_id
        }
    )

    item = response.get("Item")

    if not item:
        return "Employee ID not found."

    return f"{employee_id} has {item['balance']} leave days remaining."


# ============================================================
# Tool 2: Apply for Leave
# ============================================================

@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates.

    Example:
    ["2026-08-15", "2026-08-16"]
    """

    # Validate dates
    requested_days = len(leave_dates)

    if requested_days == 0:
        return "No leave dates provided."

    try:

        response = table.update_item(
            Key={
                "employee_id": employee_id
            },

            # Deduct balance and append leave dates
            UpdateExpression="""
                SET balance = balance - :days,
                    #history = list_append(
                        if_not_exists(#history, :empty_list),
                        :dates
                    )
            """,

            # Employee must exist AND have sufficient balance
            ConditionExpression="""
                attribute_exists(employee_id)
                AND balance >= :days
            """,

            ExpressionAttributeNames={
                "#history": "history"
            },

            ExpressionAttributeValues={
                ":days": requested_days,
                ":dates": leave_dates,
                ":empty_list": []
            },

            # Return the updated record
            ReturnValues="ALL_NEW"
        )

        new_balance = response["Attributes"]["balance"]

        return (
            f"Leave applied for {requested_days} day(s). "
            f"Remaining balance: {new_balance}."
        )

    except ClientError as e:

        error_code = e.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":

            # Check whether employee exists
            employee_response = table.get_item(
                Key={
                    "employee_id": employee_id
                }
            )

            employee = employee_response.get("Item")

            if not employee:
                return "Employee ID not found."

            available_balance = employee.get("balance", 0)

            return (
                f"Insufficient leave balance. "
                f"You requested {requested_days} day(s) "
                f"but have only {available_balance}."
            )

        # Return unexpected DynamoDB error
        return f"DynamoDB error: {str(e)}"


# ============================================================
# Tool 3: Get Leave History
# ============================================================

@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee."""

    response = table.get_item(
        Key={
            "employee_id": employee_id
        }
    )

    item = response.get("Item")

    if not item:
        return "Employee ID not found."

    history = item.get("history", [])

    if not history:
        return f"No leaves taken for {employee_id}."

    return (
        f"Leave history for {employee_id}: "
        f"{', '.join(history)}"
    )


# ============================================================
# Resource: Greeting
# ============================================================

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""

    return (
        f"Hello, {name}! "
        f"How can I assist you with leave management today?"
    )


# ============================================================
# Tool 4: Hello
# ============================================================

@mcp.tool()
def hello(name: str) -> str:
    """Say hello using the Leave Management system."""

    return (
        f"Hello {name}! "
        f"We are from the leave management system. "
        f"How can we help you?"
    )


# ============================================================
# Start MCP Server
# ============================================================

if __name__ == "__main__":

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )