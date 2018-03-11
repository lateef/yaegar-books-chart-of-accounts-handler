import sys
from awacs.aws import Policy, Statement, Allow, Principal, Action
from awacs.dynamodb import GetItem, PutItem, Query, UpdateItem
from troposphere import GetAtt, Join, Output, Parameter, Ref, Template
from troposphere.dynamodb import Table, AttributeDefinition, ProvisionedThroughput, KeySchema
from troposphere.iam import Role, Policy as iamPolicy

env = sys.argv[1]

COMPONENT_NAME = env + "YaegarBooksChartOfAccounts"

t = Template(COMPONENT_NAME)

t.add_version("2010-09-09")

shared_resources_bucket = "sharedbucketsintyaegarboo-s3bucketsharedresources-boencsukew48"
shared_resources_bucket_arn = "arn:aws:s3:::" + shared_resources_bucket

t.add_description(COMPONENT_NAME + " stacks")

chartOfAccountsMasterListTable = t.add_resource(
    Table(
        "MasterListTable",
        AttributeDefinitions=[
            AttributeDefinition(
                AttributeName="uuid",
                AttributeType="S"
            ),
            AttributeDefinition(
                AttributeName="accountTitle",
                AttributeType="S"
            )
        ],
        KeySchema=[
            KeySchema(
                AttributeName="uuid",
                KeyType="HASH"
            ),
            KeySchema(
                AttributeName="accountTitle",
                KeyType="RANGE"
            )
        ],
        ProvisionedThroughput=ProvisionedThroughput(
            ReadCapacityUnits=1,
            WriteCapacityUnits=1
        )
    )
)

chartOfAccountsByIndustryTable = t.add_resource(
    Table(
        "ByIndustryTable",
        AttributeDefinitions=[
            AttributeDefinition(
                AttributeName="uuid",
                AttributeType="S"
            )
        ],
        KeySchema=[
            KeySchema(
                AttributeName="uuid",
                KeyType="HASH"
            )
        ],
        ProvisionedThroughput=ProvisionedThroughput(
            ReadCapacityUnits=1,
            WriteCapacityUnits=1
        ),
    )
)

chartOfAccountsRole = t.add_resource(
    Role(
        "Role",
        AssumeRolePolicyDocument=Policy(
            Version="2012-10-17",
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[Action("sts", "AssumeRole")],
                    Principal=Principal(
                        "Service", ["lambda.amazonaws.com"]
                    )
                )
            ]
        ),
        Policies=[
            iamPolicy(
                PolicyName="Policy",
                PolicyDocument=Policy(
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[
                                Action("s3", "Get*"),
                                Action("s3", "List*")
                            ],
                            Resource=[
                                shared_resources_bucket_arn,
                            ]
                        ),
                        Statement(
                            Effect=Allow,
                            Action=[Action("logs", "CreateLogGroup"),
                                    Action("logs", "CreateLogStream"),
                                    Action("logs", "PutLogEvents"),
                                    Action("ec2", "CreateNetworkInterface"),
                                    Action("ec2", "DescribeNetworkInterfaces"),
                                    Action("ec2", "DeleteNetworkInterface")],
                            Resource=["*"]),
                        Statement(
                            Effect=Allow,
                            Action=[
                                Action("s3", "Get*"),
                                Action("s3", "List*"),
                                Action("s3", "Put*"),
                                Action("s3", "Delete*")
                            ],
                            Resource=[
                                shared_resources_bucket_arn + "/*"
                            ]
                        ),
                        Statement(
                            Effect=Allow,
                            Action=[GetItem, PutItem, Query, UpdateItem],
                            Resource=[
                                GetAtt(chartOfAccountsMasterListTable, "Arn")
                            ]
                        ),
                        Statement(
                            Effect=Allow,
                            Action=[GetItem, PutItem, Query, UpdateItem],
                            Resource=[
                                GetAtt(chartOfAccountsByIndustryTable, "Arn")
                            ]
                        ),
                        Statement(
                            Effect="Allow",
                            Action=[Action("logs", "*")],
                            Resource=["arn:aws:logs:*:*:*"]
                        )
                    ]
                )
            )
        ]
    )
)

t.add_output([
    Output(
        "TableNameMasterList",
        Value=Ref(chartOfAccountsMasterListTable),
        Description="Table name for chartOfAccounts",
    )
])

t.add_output([
    Output(
        "TableNameByIndustry",
        Value=Ref(chartOfAccountsByIndustryTable),
        Description="Table name for chartOfAccounts",
    )
])

print(t.to_json())
