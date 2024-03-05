#!/env/bin/py
# Script to test PDNS API Availability/Results
if __name__ != "__main__":
	raise Exception("This must be executed as a script and may not be imported.")
import sys, argparse, os
from powerdns.requests import get_zones
from shared.validators import reverse_domain_validator
from private.pdns_credentials import (
	dns_powerdns_api_url as api_url,
	dns_powerdns_api_key as api_key
)
from common.colors import print_c, bcolors
PDNS_SLAVE_TYPES = ["slave", "secondary"]

main_parser = argparse.ArgumentParser(
	prog='PowerDNS API Zone Lister',
	description='Small script that allows for PDNS API Request Method Usage',
)
main_parser.add_argument('-o', '--output-file', required=False, help="Output file for zone request results.", default=None)
main_parser.add_argument('-e', '--exclude-domains', required=False, help="Domain(s) to exclude", default=list(), nargs='+')
main_parser.add_argument('--header', required=False, help="Add a header to the file output", default=None)
main_parser.add_argument('--footer', required=False, help="Add a footer to the file output", default=None)
main_parser.add_argument('-p', '--prefix', '--add-prefix',
						 required=False, 
						 help="Add a prefix to each domain on file output", 
						 default=None
						)
main_parser.add_argument('-s', '--suffix', '--add-suffix', 
						 required=False, 
						 help="Add a suffix to each domain on file output", 
						 default=None
						)
main_parser.add_argument('-i', '--indent', 
						 required=False, 
						 help="Add indentation to each domain on file output", 
						 default=False,
						 action='store_true'
						)
main_parser.add_argument('-a', '--all-domains', 
						 required=False,
						 help="Use all domains including secondaries and slaves", 
						 default=False,
						 action='store_true'
						)
argv = main_parser.parse_args()
argv.prefix: str
argv.suffix: str
if argv.indent:
	indent_string = "\t"
else:
	indent_string = ""

domains = list()
try:
	pdns_api_request = get_zones(api_key=api_key, api_url=api_url)
except:
	raise

for pdns_d in pdns_api_request.json():
	d_type = str(pdns_d["kind"]).lower()
	pdns_d = str(pdns_d["name"])
	if pdns_d.rstrip('.') in argv.exclude_domains or (d_type in PDNS_SLAVE_TYPES and not argv.all_domains):
		continue
	if not reverse_domain_validator(pdns_d):
		domains.append(pdns_d.rstrip('.'))

# Save to file if requested
if argv.output_file:
	OUTPUT_FILEPATH = argv.output_file
	OUTPUT_DIR = os.path.dirname(argv.output_file)
	print_c(bcolors.L_BLUE, f"Saving output to file {OUTPUT_FILEPATH}")
	if os.path.isdir(OUTPUT_DIR):
		try:
			with open(OUTPUT_FILEPATH,'w+') as f:
				if argv.header and len(argv.header) > 1:
					f.write(f"{argv.header}\n")
				for d in domains:
					line_out = f"{d}"
					if argv.prefix and len(argv.prefix) > 1:
						line_out = argv.prefix + line_out
					if argv.suffix and len(argv.suffix) > 1:
						line_out = line_out + argv.suffix
					f.write(f"{indent_string}{line_out}\n")
				if argv.footer and len(argv.footer) > 1:
					f.write(f"{argv.footer}\n")
		except:
			raise
else:
	if argv.all_domains:
		print_c(bcolors.L_BLUE, "PowerDNS API Request Result (Fetching all Zones)")
	else:
		print_c(bcolors.L_BLUE, "PowerDNS API Request Result (Only Authoritative Zones)")
	print(domains)

sys.exit(0)