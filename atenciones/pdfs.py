# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import Color
# Django
from django.shortcuts import get_object_or_404
# Models
from .models import Atenciones
# pdfs
from maestros.pdfs import *

class PDFAtenciones: 
	def __init__(self, buffer, pagesize, atenciones):
		self.buffer = buffer
		self.pagesize = A4
		self.atenciones = atenciones
		if pagesize == 'Letter':
			self.pagesize = letter
		self.width, self.height = self.pagesize
 
	@staticmethod
	def _header_footer(canvas, doc):
		# Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		# HEADER
		# -- image
		image = Image('https://s3.amazonaws.com/reclutamiento/images/logopetroperu-bg-FFF.jpg')
		image.drawHeight = 0.75*inch*image.drawHeight / image.drawWidth
		image.drawWidth = 0.75*inch
		# -- title and subtitle
		title = getParagraphText('ATENCIONES', 14, 'center', True)
		# -- table
		header_table = Table([[[image],[title],[image]]], colWidths=(doc.width*0.2,doc.width*0.6,doc.width*0.2))
		header_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
											('ALIGN', (0,0), (-1,-1), 'CENTER'),
											('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0),
											('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
		w, h = header_table.wrap(doc.width, doc.topMargin)
		header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h) 
		canvas.restoreState()
 
	def print_atenciones(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(buffer,rightMargin=inch/4,leftMargin=inch/4,topMargin=80,bottomMargin=inch/4,pagesize=self.pagesize)
		elements = []
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		separador = Table([''], colWidths=[doc.width])
		separador.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
		table_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('BOTTOMPADDING', (0,0), (-1,-1), 0.025), ('TOPPADDING', (0,0), (-1,-1), 0.025)]
	
		# TABLE INFORMACION ATENCIONES
		data_table = [
			[getParagraphText('TIPO',10,'center',True),getParagraphText('DNI',10,'center',True), getParagraphText('FECHA',10,'center',True), getParagraphText('HORA INICIO',10,'center',True), getParagraphText('HORA FIN',10,'center',True)]
		]
		for atencion in self.atenciones:
			data_table.append([getParagraphText(to_lower(atencion.tipo.descripcion),10,'center',False), getParagraphText(to_lower(atencion.dni),10,'center',False), getParagraphText(str(atencion.fecha), 10,'center',False), getParagraphText(str(atencion.hora_inicio),10,'center',False), getParagraphText(str(atencion.hora_fin),10,'center',False)])
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(4,0), Color(0, 0, 0, alpha=0.1)))
		content_table = Table(data_table, colWidths=[doc.width/5.0]*5)
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)

		doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf