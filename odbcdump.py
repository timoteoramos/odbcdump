#!/usr/bin/env python3
import argparse, csv, pyodbc, sys

parser = argparse.ArgumentParser(description='Exports data from ODBC to CSV', prog='odbcdump')
parser.add_argument('--datasourcename', '-dsn', help='ODBC Data Source name', required=True)
parser.add_argument('--fileencoding', '-fe', help='Output file encoding (default: utf-8)', default='utf-8')
parser.add_argument('--metaencoding', '-me', help='DB metadata encoding (default: utf-8)', default='utf-8')
parser.add_argument('--output', '-o', help='Output file')
parser.add_argument('--password', '-pwd', help='ODBC Password')
parser.add_argument('--textencoding', '-te', help='DB text encoding (default: utf-8)', default='utf-8')
parser.add_argument('--userid', '-uid', help='ODBC User ID')
parser.add_argument('command', help='SQL command')

args = parser.parse_args()
cs = 'DSN=%s' % args.datasourcename
io = open(args.output, 'w', encoding=args.fileencoding) if args.output else sys.stdout

if args.userid:
    cs += ';UID=%s' % args.userid

if args.password:
    cs += ';PWD=%s' % args.password

try:
    conn = pyodbc.connect(cs)
    conn.setdecoding(pyodbc.SQL_CHAR, encoding=args.textencoding)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding=args.textencoding)
    conn.setdecoding(pyodbc.SQL_WMETADATA, encoding=args.metaencoding)
    conn.setencoding(encoding=args.textencoding)

    with conn.cursor() as cursor:
        writer = csv.writer(io, quoting=csv.QUOTE_NONNUMERIC)

        for row in cursor.execute(args.command):
            writer.writerow(row)

    conn.close()
finally:
    if args.output:
        io.close()
