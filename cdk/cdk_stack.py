from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw


class FriendsApiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define the DynamoDB table
        table = ddb.Table(
            self,
            "FriendsTable",
            partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING),
        )

        # Define the AWS Lambda functions
        create_friend_lambda = _lambda.Function(
            self,
            "CreateFriendHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambdas/create_friend"),
            handler="handler.handler",
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        get_all_friends_lambda = _lambda.Function(
            self,
            "GetAllFriendsHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambdas/get_all_friends"),
            handler="handler.handler",
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        # Grant the Lambda functions read/write permissions to the DynamoDB table
        table.grant_read_write_data(create_friend_lambda)
        table.grant_read_write_data(get_all_friends_lambda)

        # Define the API Gateway with the OpenAPI spec
        api = apigw.SpecRestApi(
            self,
            "FriendsApi",
            api_definition=apigw.ApiDefinition.from_asset("openapi.yaml"),
        )
        #
        # Map the Lambda functions to the API Gateway paths

        friends_resource = api.root.add_resource("friends")
        friends_resource.add_method(
            "POST", apigw.LambdaIntegration(create_friend_lambda)
        )
        friends_resource.add_method(
            "GET", apigw.LambdaIntegration(get_all_friends_lambda)
        )
