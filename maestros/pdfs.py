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
# Datetime
from datetime import datetime
# Django
from django.shortcuts import get_object_or_404
# Models
from convocatorias.models import Convocatoria, ConvocatoriaPuesto, PEQ_INT_estado_convocatoria
from usuarios.models import Persona

from maestros.services import get_lugar
  
meses = {'january':'enero','february':'febrero','march':'marzo','april':'abril','may':'mayo','june':'junio','july':'julio','august':'agosto','september':'septiembre','october':'octubre','november':'noviembre','december':'diciembre'}

def to_lower(text):
	return text.lower() if text else ''

def to_upper(text):
	return text.upper() if text else ''

class NumberedCanvas(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []
 
	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()
 
	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)
 
	def draw_page_number(self, page_count):
		# Change the position of this to wherever you want the page number to be
		self.drawRightString(109 * mm, 1 * mm + (0.2 * inch),
							 "%d - %d" % (self._pageNumber, page_count))

def getParagraphText(text, size, align, bold):
	style = ParagraphStyle(name='Normal',fontSize=size, leading=18)
	text = '<b>'+text+'</b>' if bold else text
	return Paragraph('<para align='+align+' >'+text+'</para>',style=style) if text else ''

class PDFConvocatorias: 
	def __init__(self, buffer, pagesize, uuid):
		self.buffer = buffer
		self.pagesize = A4
		self.uuid = uuid
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
		image.drawHeight = 0.95*inch*image.drawHeight / image.drawWidth
		image.drawWidth = 0.95*inch
		# -- title and subtitle
		title = getParagraphText('PROCESO DE CONVOCATORIA Y SELECCIÓN DE PERSONAL', 14, 'center', True)
		sub_title = Paragraph('<para align=center ><b> PROYECTO DE MODERNIZACION DE LA NUEVA REFINERIA DE TALARA</b></para>',styles["BodyText"])
		# -- table
		header_table = Table([[[Paragraph('<para align=center ><b>COMUNICADO DEL COMITÉ LOCAL </b></para>',styles['BodyText'])],'',''],[[image],[title, sub_title],[image]]], colWidths=(doc.width*0.2,doc.width*0.6,doc.width*0.2))
		header_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
											('ALIGN', (0,0), (-1,-1), 'CENTER'),
											('SPAN', (0,0), (2,0)),
											('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
		w, h = header_table.wrap(doc.width, doc.topMargin)
		header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h) 
  
		# Footer
		# Write footer
		# Release the canvas
		canvas.restoreState()
 
	def print_convocatoria(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(buffer,rightMargin=inch/4,leftMargin=inch/4,topMargin=125,bottomMargin=inch/4,pagesize=self.pagesize)
		elements = []
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		separador = Table([''], colWidths=[doc.width])
		separador.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
		table_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('BOTTOMPADDING', (0,0), (-1,-1), 0.025), ('TOPPADDING', (0,0), (-1,-1), 0.025)]
		convocatoria = Convocatoria.objects.get(uuid=self.uuid)
		# TITLE INFORMACION LABORAL
		title = Table([[[Paragraph('<para align=left ><b><u>I. INFORMACIÓN GENERAL</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title)
		elements.append(separador)
		# TABLE INFORMACION GENERAL
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(0,-1), Color(0, 0, 0, alpha=0.1)))
		data_table = [
			[getParagraphText('CONVOCATORIA',10,'left',True),getParagraphText(to_upper(convocatoria.nombre), 11, 'left',True)],
			[getParagraphText('CODIGO',10,'left',True),getParagraphText(to_upper(convocatoria.codigo), 11, 'left',True)],
			[getParagraphText('NOMBRE DE LA CONTRATISTA',10,'left',True), getParagraphText(convocatoria.contratista.nombre.upper() if convocatoria.contratista else '',10,'left',False)]
		]
		# -- puestos de la convocatoria
		estado = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria,estado__descripcion='en proceso').first()
		fecha_inicio = datetime.strptime(str(estado.fecha_inicio), '%Y-%m-%d') if estado else ''
		fecha_fin = datetime.strptime(str(estado.fecha_fin), '%Y-%m-%d') if estado else ''
		fecha_str = ''
		if fecha_inicio and fecha_fin:
			fecha_str = str(fecha_inicio.day)+' DE '+meses[fecha_inicio.strftime('%B').lower()].upper()+' al '+str(fecha_fin.day)+' DE '+meses[fecha_fin.strftime('%B').lower()].upper()+' DEL '+str(fecha_fin.year)
		puestos = convocatoria.convocatoriapuesto_set.all()
		table_style_with_background.append(('SPAN', (0,2), (0,(puestos.count()+1)))) if puestos.count() > 1 else ''
		for index, puesto in enumerate(puestos, 1):
			paragraph_text =  getParagraphText(u'({0}) {1} {2} {3}'.format(puesto.cantidad_vacantes, to_upper(puesto.rango.descripcion) if puesto.rango else '' , to_upper(puesto.sub_especialidad.descripcion) if puesto.sub_especialidad else '' , to_upper(puesto.especialidad.descripcion) if puesto.especialidad else '') ,10,'left',False)
			data_table.append([getParagraphText('(CANTIDAD DE VACANTES) NOMBRE DEL PUESTO',10,'left',True), paragraph_text]) if index == 1 else data_table.append(['', paragraph_text])
		data_table.append([getParagraphText('INICIO/CIERRE',10,'left',True), getParagraphText(fecha_str, 10,'left',False)])
		data_table.append([getParagraphText('REMUNERACIÓN',10,'left',True), getParagraphText(convocatoria.remuneracion.descripcion if convocatoria.remuneracion else '' ,10,'left',False)])
		data_table.append([getParagraphText('DURACIÓN DEL CONTRATO',10,'left',True), getParagraphText('SEGÚN POLITICA DE LA EMPRESA',10,'left',False)])
		data_table.append([getParagraphText('CONDICIONES ADICIONALES',10,'left',True), Paragraph('<para align=justify >'+convocatoria.condiciones_adicionales+'</para>',styles['BodyText'])])
		content_table = Table(data_table, colWidths=(doc.width*0.4,doc.width*0.6))
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)
		elements.append(separador)
		# TITLE REQUISITOS DEL PUESTO
		title = Table([[[Paragraph('<para align=left ><b><u>II. REQUISITOS DEL PUESTO</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title)
		# TABLE REQUISITOS DEL PUESTO
		table_style_with_span_bg = table_style[:]
		table_style_with_span_bg.append(('SPAN', (0,0), (2,0)))
		table_style_with_span_bg.append(('BACKGROUND',(0,0),(2,1), Color(0, 0, 0, alpha=0.1)))
		table_style_with_span_bg.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
		for puesto in puestos:
			data_table = [
				[getParagraphText(u'{0} {1} {2}'.format(to_upper(puesto.rango.descripcion) if puesto.rango else '' , to_upper(puesto.sub_especialidad.descripcion) if puesto.sub_especialidad else '' , to_upper(puesto.especialidad.descripcion) if puesto.especialidad else ''),10,'center',True),'',''],
				[getParagraphText('FORMACIÓN ACADÉMICA',8,'center',True), getParagraphText('EXPERIENCIA',8,'center',True), getParagraphText('CURSOS/CAPACITACIONES',8,'center',True)]
				]
			data_academico = puesto.peq_int_convocatoria_academico_set.all()
			data_experiencia = puesto.peq_int_convocatoria_experiencia_set.all()
			data_cursos = puesto.peq_int_convocatoria_cursos_set.all()
			data_requisitos = puesto.requisitos.all()
			cantidades = [data_academico.count(), data_experiencia.count() + data_requisitos.count(), data_cursos.count()]

			for index in range(0 ,max(cantidades)):
				row_3_data = []
				diccionario = {'academico':'','experiencia':'','cursos':''}
				# ACADEMICO
				if index < data_academico.count():
					grado = data_academico[index].grado.descripcion if data_academico[index].grado else ''
					carrera = data_academico[index].carrera.descripcion if data_academico[index].carrera else ''
					estado_grado = data_academico[index].estado_grado.descripcion if data_academico[index].estado_grado else ''
					indispensable = '(indispensable)' if data_academico[index].indispensable else ''
					diccionario['academico'] = Paragraph('<para align=justify >'+grado+' '+carrera+' '+estado_grado+' '+indispensable+'</para>',styles['BodyText'])
				row_3_data.append(diccionario['academico'])
				# EXPERIENCIA
				if index < data_experiencia.count():
					tiempo = str(data_experiencia[index].experiencia.tiempo)+' '+data_experiencia[index].experiencia.get_tipo_display() if data_experiencia[index].experiencia else ''
					rango = data_experiencia[index].rango.descripcion if data_experiencia[index].rango else ''
					sub_especialidad = data_experiencia[index].sub_especialidad.descripcion if data_experiencia[index].sub_especialidad else ''
					diccionario['experiencia'] = Paragraph('<para align=justify >('+tiempo+') '+rango+' '+sub_especialidad+'</para>',styles['BodyText'])
				else:
					index_requisito = index - data_experiencia.count()
					if (index_requisito < data_requisitos.count()):
						diccionario['experiencia'] = Paragraph('<para align=justify >'+data_requisitos[index_requisito].descripcion+'</para>',styles['BodyText'])
				row_3_data.append(diccionario['experiencia'])
				# CURSOS
				if index < data_cursos.count():
					tipo = data_cursos[index].tipo.descripcion if data_cursos[index].tipo else ''
					descripcion = data_cursos[index].descripcion if data_cursos[index].descripcion else ''
					indispensable = '(indispensable)' if data_cursos[index].indispensable else ''
					diccionario['cursos'] = Paragraph('<para align=justify ><u>'+tipo+'</u><br/><br/>'+descripcion+'<br/><br/>'+indispensable+'</para>',styles['BodyText'])
				row_3_data.append(diccionario['cursos'])
				data_table.append(row_3_data)
			
			elements.append(separador)
			content_table = Table(data_table, colWidths=[doc.width/3.0]*3)
			content_table.setStyle(TableStyle(table_style_with_span_bg))
			elements.append(content_table)

		doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf

class PDFCurriculum: 
	def __init__(self, buffer, pagesize, uuid):
		self.buffer = buffer
		self.pagesize = A4
		self.uuid = uuid
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
		title = getParagraphText('INFORMACIÓN DE LA PERSONA', 14, 'center', True)
		# -- table
		header_table = Table([[[image],[title],[image]]], colWidths=(doc.width*0.2,doc.width*0.6,doc.width*0.2))
		header_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
											('ALIGN', (0,0), (-1,-1), 'CENTER'),
											('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0),
											('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
		w, h = header_table.wrap(doc.width, doc.topMargin)
		header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h) 
  
		# Footer
		# Write footer
		# Release the canvas
		canvas.restoreState()
 
	def print_curriculum(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(buffer,rightMargin=inch/4,leftMargin=inch/4,topMargin=80,bottomMargin=inch/4,pagesize=self.pagesize)
		elements = []
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		separador = Table([''], colWidths=[doc.width])
		separador.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
		table_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('BOTTOMPADDING', (0,0), (-1,-1), 0.025), ('TOPPADDING', (0,0), (-1,-1), 0.025)]
		persona = Persona.objects.get(uuid=self.uuid)
		# TITLE INFORMACION PERSONA
		title = Table([[[Paragraph('<para align=left ><b><u>I. INFORMACIÓN PERSONAL</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title)
		# TABLE INFORMACION PERSONA
		data_table = [
			# -- nombres, apellidos, genero
			[getParagraphText('NOMBRES',10,'center',True),getParagraphText('APELLIDOS',10,'center',True), getParagraphText('GÉNERO',10,'center',True)],
			[getParagraphText(to_upper(persona.nombres),10,'center',False), getParagraphText(to_upper(persona.apellidos),10,'center',False), getParagraphText(to_upper(persona.get_genero_display()),10,'center',False)],
			# -- lugar de naciemiento, lugar de residencia, tiempo de residencia
			[getParagraphText('LUGAR DE NACIMIENTO',10,'center',True),getParagraphText('LUGAR DE RESIDENCIA',10,'center',True),getParagraphText('TIEMPO DE RESIDENCIA',10,'center',True)],
			[getParagraphText((to_upper(persona.distrito_nacimiento.descripcion) if persona.distrito_nacimiento else '') + ' ' + (to_upper(persona.provincia_nacimiento.descripcion) if persona.provincia_nacimiento else '') + ' ' + (to_upper(persona.departamento_nacimiento.descripcion) if persona.departamento_nacimiento else ''),10,'center',False), getParagraphText((to_upper(persona.distrito_residencia.descripcion) if persona.distrito_residencia else '') + ' ' + (to_upper(persona.provincia_residencia.descripcion) if persona.provincia_residencia else '') + ' ' + (to_upper(persona.departamento_residencia.descripcion) if persona.departamento_residencia else ''),10,'center',False), getParagraphText(str(persona.tiempo_residencia if persona.tiempo_residencia else 0 )+' '+( persona.get_tipo_tiempo_residencia_display()),10,'center',False),],
			# -- documento, email, estado civil
			[getParagraphText(persona.tipo_documento.descripcion.upper() if persona.tipo_documento else '',10,'center',True),getParagraphText('EMAIL',10,'center',True),getParagraphText('ESTADO CIVIL',10,'center',True)],
			[getParagraphText(persona.numero_documento,10,'center',False), getParagraphText(to_upper(persona.email),10,'center',False), getParagraphText(to_upper(persona.get_estado_civil_display()),10,'center',False)],
			# -- fecha_nacimiento, direccion, numero de licencia
			[getParagraphText('FECHA DE NACIMIENTO',10,'center',True),getParagraphText('DIRECCIÓN',10,'center',True), getParagraphText('Nº LICENCIA',10,'center',True)],
			[getParagraphText(str(persona.fecha_nacimiento.day)+' de '+to_upper(meses[persona.fecha_nacimiento.strftime('%B').lower()])+' del '+str(persona.fecha_nacimiento.year),10,'center',False), getParagraphText(to_upper(persona.direccion),10,'center',False), getParagraphText(persona.numero_licencia_conducir,10,'center',False)],
			# -- telefono, celular, discapacidad
			[getParagraphText('TELÉFONO',10,'center',True),getParagraphText('CELULAR',10,'center',True), getParagraphText('DISCAPACITADO',10,'center',True)],
			[getParagraphText(persona.telefono_fijo,10,'center',False), getParagraphText(persona.celular if persona.celular else ''+' '+persona.celular_dos if persona.celular_dos else '',10,'center',False), getParagraphText('si' if persona.discapacitado else 'no',10,'center',False)],
			# -- nacionalidad, ingles
			[getParagraphText('NACIONALIDAD',10,'center',True),getParagraphText('INGLES',10,'center',True),getParagraphText('',10,'center',True)],
			[getParagraphText(persona.nacionalidad,10,'center',False), getParagraphText(to_upper(persona.ingles.descripcion) if persona.ingles else '',10,'center',False), getParagraphText('',10,'center',False)]
		]
		table_style_with_background = table_style[:]
		len_data = len(data_table)
		for index in range(0, len_data):
			table_style_with_background.append(('BACKGROUND',(0,index),(2,index), Color(0, 0, 0, alpha=0.1))) if index % 2 == 0 else ''
		content_table = Table(data_table, colWidths=[doc.width/3.0]*3)
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)
		elements.append(separador)
		# TITLE INFORMACION EDUCATIVA
		title = Table([[[Paragraph('<para align=left ><b><u>II. INFORMACIÓN EDUCATIVA</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title)
		# TABLE INFORMACION EDUCATIVA
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(2,0), Color(0, 0, 0, alpha=0.1)))
		data_table = [
			[getParagraphText('CENTRO',10,'center',True),getParagraphText('FORMACIÓN',10,'center',True), getParagraphText('FECHA',10,'center',True)]
		]
		for educativo in persona.informacioneducativa_set.all().order_by('-fecha_inicio'):
			centro_estudio = '' if educativo.centro_estudio is None else to_upper(educativo.nombre) if to_upper(educativo.centro_estudio.descripcion) == 'otros' else to_upper(educativo.centro_estudio.descripcion)
			formacion = (educativo.grado.descripcion if educativo.grado else '') +' '+ (educativo.estado_grado.descripcion if educativo.estado_grado else '')
			formacion += ' '+(educativo.carrera.descripcion if educativo.carrera else '') if educativo.grado.orden < 3 else ''
			fecha = ''
			if educativo.hasta_actualidad:
				fecha += str(educativo.fecha_inicio.day)+' de '+to_upper(meses[educativo.fecha_inicio.strftime('%B').lower()])+' del '+str(educativo.fecha_inicio.year) + ' hasta hoy' if educativo.fecha_inicio else ''
			else:
				fecha += str(educativo.fecha_inicio.day)+' de '+to_upper(meses[educativo.fecha_inicio.strftime('%B').lower()])+' del '+str(educativo.fecha_inicio.year) if educativo.fecha_inicio else ' - '
				fecha += ' hasta '+str(educativo.fecha_fin.day)+' de '+to_upper(meses[educativo.fecha_fin.strftime('%B').lower()])+' del '+str(educativo.fecha_fin.year) if educativo.fecha_fin else ' hasta -'

			data_table.append([getParagraphText(to_upper(centro_estudio),10,'center',False), getParagraphText(to_upper(formacion),10,'center',False), getParagraphText(to_upper(fecha),10,'center',False)])

		content_table = Table(data_table, colWidths=[doc.width/3.0]*3)
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)
		elements.append(separador)
		# TITLE INFORMACION LABORAL
		title = Table([[[Paragraph('<para align=left ><b><u>III. INFORMACIÓN LABORAL</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title)
		# TABLE INFORMACION LABORAL
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(2,0), Color(0, 0, 0, alpha=0.1)))
		table_laboral = [
			[getParagraphText('EMPRESA',10,'center',True),getParagraphText('ESPECIALIDAD',10,'center',True), getParagraphText('FECHA',10,'center',True)]
		]
		for laboral in persona.informacionlaboral_set.all().order_by('-fecha_inicio'):
			empresa = '' if laboral.empresa is None else to_upper(laboral.nombre) if to_upper(laboral.empresa.descripcion) == 'otros' else to_upper(laboral.empresa.descripcion)
			formacion = (laboral.rango.descripcion if laboral.rango else '') +' '+ (laboral.especialidad.descripcion if laboral.especialidad else '')
			formacion += ' '+(laboral.sub_especialidad.descripcion if laboral.sub_especialidad else '')
			fecha = ''
			if laboral.hasta_actualidad:
				fecha += str(laboral.fecha_inicio.day)+' de '+to_upper(meses[laboral.fecha_inicio.strftime('%B').lower()])+' del '+str(laboral.fecha_inicio.year) + ' hasta hoy' if laboral.fecha_inicio else ''
			else:
				fecha += str(laboral.fecha_inicio.day)+' de '+to_upper(meses[laboral.fecha_inicio.strftime('%B').lower()])+' del '+str(laboral.fecha_inicio.year) if laboral.fecha_inicio else ' - '
				fecha += ' hasta '+str(laboral.fecha_fin.day)+' de '+to_upper(meses[laboral.fecha_fin.strftime('%B').lower()])+' del '+str(laboral.fecha_fin.year) if laboral.fecha_fin else ' hasta -'
			table_laboral.append([getParagraphText(to_upper(empresa),10,'center',False), getParagraphText(to_upper(formacion),10,'center',False), getParagraphText(to_upper(fecha),10,'center',False)])

		content_table_laboral = Table(table_laboral, colWidths=[doc.width/3.0]*3)
		content_table_laboral.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table_laboral)
		elements.append(separador)
		# TITLE INFORMACION CURSO, CAPACITACIONES, CERTIFICACIONES
		title_4 = Table([[[Paragraph('<para align=left ><b><u>IV. INFORMACIÓN CURSO, CAPACITACIONES, CERTIFICACIONES</u></b></para>',styles['BodyText'])]]], colWidths=doc.width)
		title_4.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
		elements.append(title_4)
		# TABLE INFORMACION CURSO, CAPACITACIONES, CERTIFICACIONES
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(2,0), Color(0, 0, 0, alpha=0.1)))
		table_cursos = [
			[getParagraphText('TIPO',10,'center',True),getParagraphText('NOMBRE',10,'center',True), getParagraphText('DESCRIPCIÓN',10,'center',True)]
		]
		for curso in persona.cursospostulantes_set.all():
			table_cursos.append([getParagraphText(to_upper(curso.tipo.descripcion) if curso.tipo else '' ,10,'center',False), getParagraphText(to_upper(curso.nombre.descripcion) if curso.nombre else '',10,'center',False), getParagraphText(to_upper(curso.descripcion),10,'center',False)])

		content_table_cursos = Table(table_cursos, colWidths=[doc.width/3.0]*3)
		content_table_cursos.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table_cursos)
		elements.append(separador)

		doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf

class PDFPostulantes: 

	def __init__(self, buffer, pagesize, registros, title):
		self.buffer = buffer
		self.pagesize = A4
		self.registros = registros
		self.title = title
		if pagesize == 'Letter':
			self.pagesize = letter
		self.width, self.height = self.pagesize
 
	def _header_footer(self, canvas, doc):
		# Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		# HEADER
		# -- image
		image = Image('https://s3.amazonaws.com/reclutamiento/images/logopetroperu-bg-FFF.jpg')
		image.drawHeight = 0.75*inch*image.drawHeight / image.drawWidth
		image.drawWidth = 0.75*inch
		# -- title and subtitle
		title = getParagraphText(to_upper(self.title), 14, 'center', True)
		sub_title = Paragraph('<para align=center ><b> INFORMACIÓN GENERAL DE LOS POSTULANTES</b></para>',styles["BodyText"])
		# -- table
		header_table = Table([[[image],[title, sub_title],[image]]], colWidths=(doc.width*0.2,doc.width*0.6,doc.width*0.2))
		header_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
											('ALIGN', (0,0), (-1,-1), 'CENTER'),
											('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
		w, h = header_table.wrap(doc.width, doc.topMargin)
		header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h) 
		# Footer
		# Write footer
		# Release the canvas
		canvas.restoreState()
 
	def print_informacion_general(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(buffer,rightMargin=inch/4,leftMargin=inch/4,topMargin=80,bottomMargin=inch/4,pagesize=self.pagesize)
		elements = []
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		separador = Table([''], colWidths=[doc.width])
		separador.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
		table_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('BOTTOMPADDING', (0,0), (-1,-1), 0.025), ('TOPPADDING', (0,0), (-1,-1), 0.025)]
		# TABLE INFORMACIÓN GENERAL DE PERSONAS
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(4,0), Color(0, 0, 0, alpha=0.1)))
		data_table = [
			[getParagraphText('NOMBRES',10,'center',True), getParagraphText('APELLIDOS',10,'center',True),getParagraphText('LUGAR',10,'center',True), getParagraphText('PORCENTAJE',10,'center',True), getParagraphText('CELULAR',10,'center',True)]
		]
		for estado_postulacion in self.registros:
			lugar = get_lugar(estado_postulacion.postulacion.persona)
			nombre_lugar = ''
			if lugar == 2:
				nombre_lugar = 'TALAREÑO'
			elif lugar == 1:
				nombre_lugar = 'REGIÓN'
			data_table.append([getParagraphText(to_upper(estado_postulacion.postulacion.persona.nombres),10,'center',False), getParagraphText(to_upper(estado_postulacion.postulacion.persona.apellidos),10,'center',False), getParagraphText(nombre_lugar,10,'center',False), getParagraphText(to_upper(estado_postulacion.postulacion.rango.descripcion) if estado_postulacion.postulacion.rango else '',10,'center',False), getParagraphText(estado_postulacion.postulacion.persona.celular+' '+ estado_postulacion.postulacion.persona.celular_dos,10,'center',False),])

		content_table = Table(data_table, colWidths=[doc.width/5.0]*5)
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)

		doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf

	def print_pase_de_ingreso(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(buffer,rightMargin=inch/4,leftMargin=inch/4,topMargin=80,bottomMargin=inch/4,pagesize=self.pagesize)
		elements = []
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		separador = Table([''], colWidths=[doc.width])
		separador.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
		table_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ('BOTTOMPADDING', (0,0), (-1,-1), 0.025), ('TOPPADDING', (0,0), (-1,-1), 0.025)]
		# TABLE INFORMACIÓN GENERAL DE PERSONAS
		table_style_with_background = table_style[:]
		table_style_with_background.append(('BACKGROUND',(0,0),(4,0), Color(0, 0, 0, alpha=0.1)))
		data_table = [
			[getParagraphText('CRITERIO',10,'center',True), getParagraphText('NOMBRES',10,'center',True), getParagraphText('APELLIDOS',10,'center',True),getParagraphText('LUGAR',10,'center',True), getParagraphText('CELULAR',10,'center',True)]
		]
		for registro in self.registros:
			lugar = get_lugar(registro.persona)
			nombre_lugar = ''
			if lugar == 2:
				nombre_lugar = 'TALAREÑO'
			elif lugar == 1:
				nombre_lugar = 'REGIÓN'
			data_table.append([getParagraphText(to_upper(registro.criterio_aprobacion.alias if registro.criterio_aprobacion else ''),10,'center',False), getParagraphText(to_upper(registro.persona.nombres if registro.persona else ''),10,'center',False), getParagraphText(to_upper(registro.persona.apellidos if registro.persona else ''),10,'center',False), getParagraphText(nombre_lugar,10,'center',False), getParagraphText(str(registro.persona.celular if registro.persona else '')+' '+ str(registro.persona.celular_dos if registro.persona else ''),10,'center',False)])

		content_table = Table(data_table, colWidths=[doc.width/5.0]*5)
		content_table.setStyle(TableStyle(table_style_with_background))
		elements.append(content_table)

		doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf