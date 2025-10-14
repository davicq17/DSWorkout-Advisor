from api.db import pool
from fpdf import FPDF

## ruta para generar y descargar el informe
@app.route('/generarPDF')
def generarPDF():
    try:
        cur=mysql.connection.cursor()
        ## consulta de todas las evaluaciones
        cur.execute('''SELECT evaluation.id_evaluation,
                    cliente.name AS cliente, 
                    profesional.name AS profesional,
                    routine.nombre, 
                    evaluation.fech_evaluation 
                    FROM evaluation 
                    JOIN usuarios AS cliente on evaluation.id_cliente = cliente.id 
                    JOIN routine on  evaluation.id_routine = routine.id_routine 
                    JOIN usuarios AS profesional on evaluation.id_prof= profesional.id
                    WHERE evaluation.fech_evaluation >= now() - INTERVAL 7 DAY''')
        rv = cur.fetchall()
        payload=[]
        content={}
        for result in rv:
            content={'id_evaluation':result[0],'cliente':result[1],'profesional':result[2],'nombre_rutina':result[3],'fecha_evaluacion':result[4]}
            payload.append(content)
        ## segunda consulta, numero de usuarios activos
        cur.execute("SELECT count(usuarios.id) FROM usuarios WHERE usuarios.status = 1")
        US= cur.fetchone()
        ## tercera consulta de las evaluaciones hechas en la ultima semana
        cur.execute("SELECT count(evaluation.id_evaluation)  FROM evaluation WHERE evaluation.fech_evaluation >= now() - INTERVAL 7 DAY")
        ev= cur.fetchone()
        ## cuarta consulta, cantidad  de tipos de ejercicios 
        cur.execute("SELECT workout.tipo, count(workout.id_workout) FROM workout  GROUP BY workout.tipo;")
        wk= cur.fetchall()
        payload2=[]
        content2={}
        for result in wk:
            content2={'tipo':result[0], 'workouts':result[1]}
            payload2.append(content2) 
        cur.close()
        ## creacion del pdf
        pdf = FPDF()
        pdf.add_page()
        ## sección de la evaluacion
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(page_width, 10, txt='Reporte de Evaluaciones',ln=True, align='C')
        pdf.set_font('Arial', 'B', 12)
        ## evaluaciones de la semana
        pdf.cell(0,10, txt='Usuarios activos: '+str(US[0]), ln=True)
        pdf.cell(0, 10, txt='Evaluaciones realizadas en la última semana: '+str(ev[0]), ln=False)
        col_width= page_width/6
        col_width2= page_width/3
        pdf.ln(10)
        th=pdf.font_size
        ## encabezados de la tabla de las evaluaciones
        pdf.cell(col_width, th, txt='# Evaluación', border=1)
        pdf.cell(col_width, th, txt='Cliente', border=1)
        pdf.cell(col_width, th, txt='Profesional', border=1)
        pdf.cell(col_width2, th, txt='Rutina', border=1)
        pdf.cell(col_width, th, txt='Fecha', border=1)
        pdf.ln(th)
        pdf.set_font('Arial', '', 12)
        for row in payload:
            ##print("fila escrita")
            pdf.cell(col_width,th, str(row['id_evaluation']), border=1)
            pdf.cell(col_width,th, row['cliente'], border=1)
            pdf.cell(col_width,th, row['profesional'], border=1)
            pdf.cell(col_width2,th, row['nombre_rutina'], border=1)
            pdf.cell(col_width,th, str(row['fecha_evaluacion']), border=1)
            pdf.ln(th)
        pdf.ln(10)
        ## sección de ejercicio
        pdf.set_font('Arial','B', 16)
        pdf.cell(page_width,10,txt='Reporte de Ejercicios',ln=True, align='C')
        pdf.set_font('Arial','B',12)
        ## encabezado de la tabla ejercicios 
        col_width = page_width/2
        pdf.ln(5)  
        th = pdf.font_size
        headers = ['Tipo','Cantidad']
        for header in headers:
            pdf.cell(col_width,th,txt=header,border=1, align='C')
        pdf.ln(th)
        pdf.set_font('Arial','',12)
        for row in payload2:
            pdf.cell(col_width,th, row['tipo'], border=1,align='C')
            pdf.cell(col_width,th, str(row['workouts']), border=1,align='C')
            pdf.ln(th)
        pdf.ln(10)
        pdf.set_font('Arial','',10)
        pdf.cell(page_width,0.0, txt='Fin de reporte', align='C')

        pdf_output = io.BytesIO()
        pdf.output(dest='S')  # Guardar el PDF en una cadena de bytes
        pdf_output.write(pdf.output(dest='S').encode('latin1'))  # Escribir el contenido PDF en BytesIO
        pdf_output.seek(0)

        #print("PDF listo para mandar")
        return send_file(pdf_output, as_attachment=True, download_name='Informe.pdf', mimetype='application/pdf')
    except Exception as e:
        return f"Se produjo un error: {str(e)}"