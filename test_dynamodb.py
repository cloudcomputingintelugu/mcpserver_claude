import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

table = dynamodb.Table("EmployeeLeaves")

response = table.get_item(
    Key={
        "employee_id": "E001"
    }
)

print(response.get("Item"))