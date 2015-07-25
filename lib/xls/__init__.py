import xlwt
import StringIO
import datetime

from django.http import HttpResponse

styleregr = xlwt.easyxf('')
styledate = xlwt.easyxf(num_format_str='dd/mm/yyyy')
stylebold = xlwt.easyxf('font: bold on')

class Column(object):
	def __init__(self, name, valuefunc):
		self.name = name
		self.valuefunc = valuefunc

def make(columns, data):
	wb = xlwt.Workbook()
	ws = wb.add_sheet('PHRENDS')

	colnum = 0
	for column in columns:
		ws.write(0, colnum, column.name, stylebold)
		colnum += 1

	rownum = 1
	for row in data:
		colnum = 0
		for column in columns:
			val = column.valuefunc(row)
			if (isinstance(val, datetime.datetime)):
				ws.write(rownum, colnum, val, styledate)
			else:
				ws.write(rownum, colnum, val, styleregr)
			colnum += 1
		rownum += 1

	output = StringIO.StringIO()

	wb.save(output)

	data = output.getvalue()

	output.close()

	return data

class XlsResponse(HttpResponse):
	def __init__(self, columns, data, filename):
		xlsdata = make(columns, data)

		HttpResponse.__init__(self, xlsdata)
		self['Content-Type'] = "application/vnd.ms-excel"
		self['Content-Disposition'] = "attachment; filename=%s" % filename