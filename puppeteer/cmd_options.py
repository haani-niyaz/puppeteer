import argparse


def main():

	parser = argparse.ArgumentParser(prog='puppeteer',description='Utility to manage ansible workflow')

	subparsers = parser.add_subparsers(dest='sub_cmd',help='sub-command help')

	# Tag parser	
	parser_tag = subparsers.add_parser('tag', help='a help')
	parser_tag.add_argument('version', help='version help')
	parser_tag.add_argument('-r','--role', help='role help')
	parser_tag.add_argument('-e','--env', help='role help')

	# Init parser
	parser_init = subparsers.add_parser('init')

	return parser.parse_args()

