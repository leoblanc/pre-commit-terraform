import terraform_validate
import unittest
import os
import sys

class TestAWSResources(unittest.TestCase):

    def setUp(self):
        # terralint.sh provides the directory of the terraform files as argument
        terraform_directory = sys.argv[1]

        # Tell the module where to find your terraform configuration folder
        self.path = terraform_directory
        self.v = terraform_validate.Validator(self.path)

    def test_tags(self):
        # Assert that all resources of these types have the correct tags
        # NOTE: This is a small sample (proof-of-concept list)
        tagged_resources = ["aws_instance","aws_ebs_volume","aws_lambda_function"]
        required_tags = ["Name","Version","Owner"]
        self.v.resources(tagged_resources).property('tags').should_have_properties(required_tags)

    def test_naming(self):
        # Assert that all resources of these types doesnt include/repeat the resource type on the resource name
        # NOTE: This is a small sample (proof-of-concept list)
        aws_resources = ["aws_lambda_function", "aws_iam_role"]
        resource_types = ["lambda_function", "iam_role"]
        self.v.resources(aws_resources).property('name').list_should_not_contain(resource_types)
        # NOTE: The above checking is just for the "name" property of the resource.
        #       For the actual resoruce name the function "name_should_match_regex" could be used.

if __name__ == '__main__':
    # Execute tests and return success to shell (for pre-commit)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAWSResources)
    ret = not unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful()
    sys.exit(ret)
