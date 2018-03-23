import alertlogiccli.command

import requests
import json

class ScannerEstimation(alertlogiccli.command.Command):
    """Command to get installation status from saturn"""

    def configure_parser(self, subparsers):
        parser = subparsers.add_parser("scanner_estimation", help="gets scanner estimation from skaletor")
        parser.set_defaults(command=self)
        parser.add_argument("--deployment_id", help="deployment id")
        parser.add_argument("--vpc_key", help="vpc key")

    def execute(self, context):
        args = context.get_final_args()
        skaletor = context.get_services().skaletor
        try:
            if args["vpc_key"] is not None and args["deployment_id"] is not None:
                response = skaletor.get_scanners(
                    account_id = args["account_id"],
                    deployment_id = args["deployment_id"],
                    vpc_key = args["vpc_key"]
                )
                response.raise_for_status()
            elif args["vpc_key"] is None and args["deployment_id"] is not None:
                response = skaletor.get_scanners(
                    account_id = args["account_id"],
                    deployment_id = args["deployment_id"]
                )
                response.raise_for_status()
            elif args["vpc_key"] is not None and args["deployment_id"] is None:
                response = skaletor.get_scanners(
                    account_id = args["account_id"],
                    vpc_key = args["vpc_key"]
                )
            else:
                response = skaletor.get_scanners(
                    account_id = args["account_id"]
                )
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise alertlogiccli.command.InvalidHTTPResponse("scanner_estimation", e.message)
        return json.dumps(response.json(), sort_keys=True, separators=(',',':'))