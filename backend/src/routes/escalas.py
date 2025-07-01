from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import io
import os
from flask_cors import cross_origin

escalas_bp = Blueprint('escalas', __name__)

# Configurações de e-mail (você pode configurar com suas credenciais)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "seu_email@gmail.com"  # Configure com seu e-mail
EMAIL_PASSWORD = "sua_senha_app"    # Configure com sua senha de app

@escalas_bp.route('/enviar-escalas', methods=['POST'])
@cross_origin()
def enviar_escalas():
    try:
        data = request.get_json()
        escalas = data.get('escalas', [])
        
        if not escalas:
            return jsonify({'error': 'Nenhuma escala fornecida'}), 400
        
        # Agrupar escalas por cooperado
        escalas_por_cooperado = {}
        for escala in escalas:
            cooperado = escala.get('cooperado')
            email = escala.get('email')
            
            if not cooperado or not email:
                continue
                
            if cooperado not in escalas_por_cooperado:
                escalas_por_cooperado[cooperado] = {
                    'email': email,
                    'escalas': []
                }
            
            escalas_por_cooperado[cooperado]['escalas'].append(escala)
        
        # Enviar e-mail para cada cooperado
        enviados = 0
        erros = []
        
        for cooperado, dados in escalas_por_cooperado.items():
            try:
                # Criar planilha individual
                df = pd.DataFrame(dados['escalas'])
                excel_buffer = io.BytesIO()
                df.to_excel(excel_buffer, index=False, sheet_name='Escala')
                excel_buffer.seek(0)
                
                # Enviar e-mail
                msg = MIMEMultipart()
                msg['From'] = EMAIL_USER
                msg['To'] = dados['email']
                msg['Subject'] = f'Escala de Trabalho - {cooperado}'
                
                body = f"""
                Olá {cooperado},
                
                Segue em anexo sua escala de trabalho.
                
                Atenciosamente,
                COOPEX
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Anexar planilha
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(excel_buffer.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="escala_{cooperado.replace(" ", "_")}.xlsx"'
                )
                msg.attach(part)
                
                # Enviar e-mail
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(EMAIL_USER, dados['email'], text)
                server.quit()
                
                enviados += 1
                
            except Exception as e:
                erros.append(f'Erro ao enviar para {cooperado}: {str(e)}')
        
        return jsonify({
            'success': True,
            'enviados': enviados,
            'erros': erros
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escalas_bp.route('/processar-planilha', methods=['POST'])
@cross_origin()
def processar_planilha():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Ler planilha Excel
        df = pd.read_excel(file)
        
        # Converter para lista de dicionários
        escalas = df.to_dict('records')
        
        # Limpar dados vazios
        escalas_limpas = []
        for escala in escalas:
            if pd.notna(escala.get('Nome Cooperado')) and escala.get('Nome Cooperado').strip():
                escalas_limpas.append({
                    'cooperado': str(escala.get('Nome Cooperado', '')).strip(),
                    'email': str(escala.get('Email', '')).strip(),
                    'data': str(escala.get('Data', '')).strip(),
                    'turno': str(escala.get('Turno', '')).strip(),
                    'horario': str(escala.get('Horário', '')).strip(),
                    'contrato': str(escala.get('Nome Contrato', '')).strip()
                })
        
        return jsonify({
            'success': True,
            'escalas': escalas_limpas,
            'total': len(escalas_limpas)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

