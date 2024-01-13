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
main_parser.add_argument('-d', '--dns-address', required=True, help="DNS Resolver Address to Forward Internal Zones To")
main_parser.add_argument('-p', '--dns-port', required=False, help="DNS Resolver Port to Forward Internal Zones To", default=53)
argv = main_parser.parse_args()
try: int(argv.dns_port)
except: raise TypeError("DNS Port must be an Integer.")

domains = list()
try:
	pdns_api_request = get_zones(api_key=api_key, api_url=api_url)
except:
	raise

for pdns_d in pdns_api_request.json():
	d_type = str(pdns_d["kind"]).lower()
	pdns_d = str(pdns_d["name"])
	if pdns_d.rstrip('.') in argv.exclude_domains or d_type in PDNS_SLAVE_TYPES: continue
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
				f.write(f"server:\n")
				for d in domains:
					f.write(f"\tprivate-domain: {d}\n")
				for d in domains:
					f.write(f"forward-zone:\n")
					f.write(f"\tname: {d}\n")
					f.write(f"\tforward-addr: {argv.dns_address}@{argv.dns_port}\n")
		except:
			raise
else:
	print_c(bcolors.L_BLUE, "PowerDNS API Request Result (Only Authoritative Zones)")
	print(f"server:")
	for d in domains:
		print(f"\tprivate-domain: {d}")
	for d in domains:
		print(f"forward-zone:")
		print(f"\tname: {d}")
		print(f"\tforward-addr: {argv.dns_address}@{argv.dns_port}")

sys.exit(0)