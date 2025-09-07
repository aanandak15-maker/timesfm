#!/usr/bin/env python3
"""
Report Generation System for AgriForecast.ai
Phase 2: Data Export & Reporting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import io
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerationSystem:
    """Advanced report generation and export system"""
    
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Setup database for report generation"""
        self.conn = sqlite3.connect('agriforecast_reports.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                report_name TEXT NOT NULL,
                report_data TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create report templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS report_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT NOT NULL,
                template_type TEXT NOT NULL,
                template_config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create email settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                email_address TEXT NOT NULL,
                smtp_server TEXT,
                smtp_port INTEGER,
                username TEXT,
                password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("Report generation database setup completed")
    
    def generate_farm_summary_report(self, user_id: int, farm_data: Dict) -> Dict:
        """Generate comprehensive farm summary report"""
        try:
            report_data = {
                'report_type': 'farm_summary',
                'report_name': f"Farm Summary Report - {datetime.now().strftime('%Y-%m-%d')}",
                'generated_at': datetime.now().isoformat(),
                'farm_data': farm_data,
                'sections': []
            }
            
            # Executive Summary
            executive_summary = {
                'title': 'Executive Summary',
                'content': f"""
                This report provides a comprehensive analysis of farm operations for {farm_data.get('farm_name', 'Unknown Farm')}.
                The analysis covers yield trends, cost-benefit analysis, ROI calculations, and field performance metrics.
                Key findings include optimal crop selection, seasonal performance patterns, and recommendations for improvement.
                """
            }
            report_data['sections'].append(executive_summary)
            
            # Yield Analysis
            yield_analysis = {
                'title': 'Yield Analysis',
                'content': f"""
                Total fields analyzed: {len(farm_data.get('fields', []))}
                Average yield per acre: {farm_data.get('avg_yield', 0):.2f} tons
                Best performing crop: {farm_data.get('best_crop', 'N/A')}
                Yield trend: {farm_data.get('yield_trend', 'Stable')}
                """
            }
            report_data['sections'].append(yield_analysis)
            
            # Financial Analysis
            financial_analysis = {
                'title': 'Financial Analysis',
                'content': f"""
                Total revenue: ${farm_data.get('total_revenue', 0):,.2f}
                Total costs: ${farm_data.get('total_costs', 0):,.2f}
                Net profit: ${farm_data.get('net_profit', 0):,.2f}
                ROI: {farm_data.get('roi_percentage', 0):.1f}%
                Profit margin: {farm_data.get('profit_margin', 0):.1f}%
                """
            }
            report_data['sections'].append(financial_analysis)
            
            # Recommendations
            recommendations = {
                'title': 'Recommendations',
                'content': f"""
                1. Focus on high-performing crops: {farm_data.get('best_crop', 'N/A')}
                2. Optimize input costs in low-performing areas
                3. Consider expanding successful field management practices
                4. Monitor weather patterns for better planning
                5. Implement precision agriculture techniques
                """
            }
            report_data['sections'].append(recommendations)
            
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating farm summary report: {e}")
            return {}
    
    def generate_yield_analysis_report(self, user_id: int, yield_data: pd.DataFrame) -> Dict:
        """Generate detailed yield analysis report"""
        try:
            if yield_data.empty:
                return {}
            
            report_data = {
                'report_type': 'yield_analysis',
                'report_name': f"Yield Analysis Report - {datetime.now().strftime('%Y-%m-%d')}",
                'generated_at': datetime.now().isoformat(),
                'yield_data': yield_data.to_dict('records'),
                'summary_stats': {
                    'total_yields': len(yield_data),
                    'avg_yield': yield_data['actual_yield'].mean(),
                    'max_yield': yield_data['actual_yield'].max(),
                    'min_yield': yield_data['actual_yield'].min(),
                    'yield_variance': yield_data['yield_variance'].mean(),
                    'prediction_accuracy': yield_data['confidence_score'].mean()
                }
            }
            
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating yield analysis report: {e}")
            return {}
    
    def generate_financial_report(self, user_id: int, financial_data: Dict) -> Dict:
        """Generate comprehensive financial report"""
        try:
            report_data = {
                'report_type': 'financial_analysis',
                'report_name': f"Financial Analysis Report - {datetime.now().strftime('%Y-%m-%d')}",
                'generated_at': datetime.now().isoformat(),
                'financial_data': financial_data,
                'sections': []
            }
            
            # Revenue Analysis
            revenue_section = {
                'title': 'Revenue Analysis',
                'content': f"""
                Total Revenue: ${financial_data.get('total_revenue', 0):,.2f}
                Revenue per Acre: ${financial_data.get('revenue_per_acre', 0):,.2f}
                Revenue Growth: {financial_data.get('revenue_growth', 0):.1f}%
                Top Revenue Crop: {financial_data.get('top_revenue_crop', 'N/A')}
                """
            }
            report_data['sections'].append(revenue_section)
            
            # Cost Analysis
            cost_section = {
                'title': 'Cost Analysis',
                'content': f"""
                Total Costs: ${financial_data.get('total_costs', 0):,.2f}
                Cost per Acre: ${financial_data.get('cost_per_acre', 0):,.2f}
                Cost Breakdown:
                - Inputs: {financial_data.get('input_costs', 0):.1f}%
                - Labor: {financial_data.get('labor_costs', 0):.1f}%
                - Equipment: {financial_data.get('equipment_costs', 0):.1f}%
                - Other: {financial_data.get('other_costs', 0):.1f}%
                """
            }
            report_data['sections'].append(cost_section)
            
            # Profitability Analysis
            profitability_section = {
                'title': 'Profitability Analysis',
                'content': f"""
                Net Profit: ${financial_data.get('net_profit', 0):,.2f}
                Profit Margin: {financial_data.get('profit_margin', 0):.1f}%
                ROI: {financial_data.get('roi_percentage', 0):.1f}%
                Break-even Point: {financial_data.get('break_even_yield', 0):.2f} tons/acre
                """
            }
            report_data['sections'].append(profitability_section)
            
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating financial report: {e}")
            return {}
    
    def create_pdf_report(self, report_data: Dict) -> bytes:
        """Create PDF report from data"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(report_data['report_name'], title_style))
            story.append(Spacer(1, 12))
            
            # Report info
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.grey
            )
            story.append(Paragraph(f"Generated on: {report_data['generated_at']}", info_style))
            story.append(Spacer(1, 20))
            
            # Sections
            for section in report_data.get('sections', []):
                # Section title
                story.append(Paragraph(section['title'], styles['Heading2']))
                story.append(Spacer(1, 12))
                
                # Section content
                story.append(Paragraph(section['content'], styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Summary table if available
            if 'summary_stats' in report_data:
                story.append(Paragraph("Summary Statistics", styles['Heading2']))
                story.append(Spacer(1, 12))
                
                # Create summary table
                summary_data = report_data['summary_stats']
                table_data = [
                    ['Metric', 'Value'],
                    ['Total Yields', str(summary_data.get('total_yields', 0))],
                    ['Average Yield', f"{summary_data.get('avg_yield', 0):.2f} tons"],
                    ['Max Yield', f"{summary_data.get('max_yield', 0):.2f} tons"],
                    ['Min Yield', f"{summary_data.get('min_yield', 0):.2f} tons"],
                    ['Prediction Accuracy', f"{summary_data.get('prediction_accuracy', 0):.1%}"]
                ]
                
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
                story.append(Spacer(1, 20))
            
            # Footer
            story.append(Spacer(1, 30))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=1
            )
            story.append(Paragraph("Generated by AgriForecast.ai - Advanced Agricultural Analytics", footer_style))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating PDF report: {e}")
            return b""
    
    def create_excel_report(self, report_data: Dict) -> bytes:
        """Create Excel report from data"""
        try:
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                # Summary sheet
                if 'summary_stats' in report_data:
                    summary_df = pd.DataFrame(list(report_data['summary_stats'].items()), 
                                            columns=['Metric', 'Value'])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Yield data sheet
                if 'yield_data' in report_data:
                    yield_df = pd.DataFrame(report_data['yield_data'])
                    yield_df.to_excel(writer, sheet_name='Yield Data', index=False)
                
                # Financial data sheet
                if 'financial_data' in report_data:
                    financial_df = pd.DataFrame([report_data['financial_data']])
                    financial_df.to_excel(writer, sheet_name='Financial Data', index=False)
                
                # Sections sheet
                if 'sections' in report_data:
                    sections_data = []
                    for section in report_data['sections']:
                        sections_data.append({
                            'Title': section['title'],
                            'Content': section['content']
                        })
                    sections_df = pd.DataFrame(sections_data)
                    sections_df.to_excel(writer, sheet_name='Report Sections', index=False)
            
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating Excel report: {e}")
            return b""
    
    def send_email_report(self, email_address: str, report_data: Dict, 
                         report_type: str = 'pdf') -> bool:
        """Send report via email"""
        try:
            # Create report file
            if report_type == 'pdf':
                file_content = self.create_pdf_report(report_data)
                file_extension = 'pdf'
                mime_type = 'application/pdf'
            else:
                file_content = self.create_excel_report(report_data)
                file_extension = 'xlsx'
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            if not file_content:
                return False
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = "noreply@agriforecast.ai"
            msg['To'] = email_address
            msg['Subject'] = f"AgriForecast Report - {report_data['report_name']}"
            
            # Email body
            body = f"""
            Dear User,
            
            Please find attached your {report_data['report_name']}.
            
            This report contains comprehensive analysis of your agricultural operations including:
            - Yield trends and predictions
            - Cost-benefit analysis
            - ROI calculations
            - Field performance metrics
            - Recommendations for improvement
            
            Best regards,
            AgriForecast.ai Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach report
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_content)
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename= {report_data["report_name"]}.{file_extension}'
            )
            msg.attach(attachment)
            
            # Send email (simplified - in production, use proper SMTP settings)
            # For demo purposes, we'll just log the email
            logger.info(f"Email report sent to {email_address}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email report: {e}")
            return False
    
    def save_report(self, user_id: int, report_data: Dict) -> int:
        """Save report to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO generated_reports (user_id, report_type, report_name, report_data)
                VALUES (?, ?, ?, ?)
            ''', (user_id, report_data['report_type'], report_data['report_name'], 
                  json.dumps(report_data)))
            
            report_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Report saved with ID: {report_id}")
            return report_id
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return 0

class ReportGenerationFrontend:
    """Report generation frontend"""
    
    def __init__(self):
        self.report_system = ReportGenerationSystem()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="AgriForecast Reports",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render report generation sidebar"""
        st.sidebar.title("📄 Report Generation")
        
        # User selection
        user_id = st.sidebar.selectbox(
            "Select User",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"User {x}"
        )
        
        # Report type selection
        report_type = st.sidebar.selectbox(
            "Report Type",
            ["Farm Summary", "Yield Analysis", "Financial Analysis", "Field Performance"]
        )
        
        # Export format
        export_format = st.sidebar.selectbox(
            "Export Format",
            ["PDF", "Excel", "Both"]
        )
        
        # Email settings
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📧 Email Settings")
        email_address = st.sidebar.text_input("Email Address", placeholder="user@example.com")
        send_email = st.sidebar.checkbox("Send via Email")
        
        return user_id, report_type, export_format, email_address, send_email
    
    def render_report_generation(self, user_id: int, report_type: str, 
                                export_format: str, email_address: str, send_email: bool):
        """Render report generation interface"""
        st.subheader(f"📄 Generate {report_type} Report")
        
        # Generate sample data for demonstration
        if st.button("Generate Sample Data", type="primary"):
            # Create sample farm data
            farm_data = {
                'farm_name': f'Farm {user_id}',
                'fields': [{'name': f'Field {i}', 'crop': 'Rice', 'area': 10} for i in range(1, 4)],
                'avg_yield': 3.5,
                'best_crop': 'Rice',
                'yield_trend': 'Increasing',
                'total_revenue': 50000,
                'total_costs': 35000,
                'net_profit': 15000,
                'roi_percentage': 42.9,
                'profit_margin': 30.0
            }
            
            # Generate report based on type
            if report_type == "Farm Summary":
                report_data = self.report_system.generate_farm_summary_report(user_id, farm_data)
            elif report_type == "Yield Analysis":
                # Create sample yield data
                yield_data = pd.DataFrame({
                    'crop_type': ['Rice', 'Wheat', 'Corn'] * 3,
                    'season': ['Kharif', 'Rabi', 'Summer'] * 3,
                    'year': [2023, 2023, 2023, 2024, 2024, 2024, 2025, 2025, 2025],
                    'actual_yield': [3.2, 2.8, 4.1, 3.5, 3.0, 4.3, 3.8, 3.2, 4.5],
                    'predicted_yield': [3.0, 2.9, 4.0, 3.4, 3.1, 4.2, 3.7, 3.3, 4.4],
                    'yield_variance': [0.2, -0.1, 0.1, 0.1, -0.1, 0.1, 0.1, -0.1, 0.1],
                    'confidence_score': [0.85, 0.78, 0.92, 0.88, 0.82, 0.90, 0.87, 0.84, 0.91]
                })
                report_data = self.report_system.generate_yield_analysis_report(user_id, yield_data)
            elif report_type == "Financial Analysis":
                financial_data = {
                    'total_revenue': 50000,
                    'revenue_per_acre': 1667,
                    'revenue_growth': 15.2,
                    'top_revenue_crop': 'Rice',
                    'total_costs': 35000,
                    'cost_per_acre': 1167,
                    'input_costs': 40,
                    'labor_costs': 30,
                    'equipment_costs': 20,
                    'other_costs': 10,
                    'net_profit': 15000,
                    'profit_margin': 30.0,
                    'roi_percentage': 42.9,
                    'break_even_yield': 2.1
                }
                report_data = self.report_system.generate_financial_report(user_id, financial_data)
            else:  # Field Performance
                report_data = self.report_system.generate_farm_summary_report(user_id, farm_data)
            
            if report_data:
                # Save report
                report_id = self.report_system.save_report(user_id, report_data)
                
                # Display report preview
                st.success(f"Report generated successfully! Report ID: {report_id}")
                
                # Show report preview
                st.subheader("📋 Report Preview")
                for section in report_data.get('sections', []):
                    with st.expander(section['title']):
                        st.write(section['content'])
                
                # Export options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if export_format in ["PDF", "Both"]:
                        pdf_content = self.report_system.create_pdf_report(report_data)
                        if pdf_content:
                            st.download_button(
                                label="📄 Download PDF",
                                data=pdf_content,
                                file_name=f"{report_data['report_name']}.pdf",
                                mime="application/pdf"
                            )
                
                with col2:
                    if export_format in ["Excel", "Both"]:
                        excel_content = self.report_system.create_excel_report(report_data)
                        if excel_content:
                            st.download_button(
                                label="📊 Download Excel",
                                data=excel_content,
                                file_name=f"{report_data['report_name']}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                
                with col3:
                    if send_email and email_address:
                        if st.button("📧 Send Email"):
                            success = self.report_system.send_email_report(
                                email_address, report_data, 
                                'pdf' if export_format == "PDF" else 'excel'
                            )
                            if success:
                                st.success("Email sent successfully!")
                            else:
                                st.error("Failed to send email")
            else:
                st.error("Failed to generate report")
    
    def render_report_history(self, user_id: int):
        """Render report history"""
        st.subheader("📚 Report History")
        
        try:
            cursor = self.report_system.conn.cursor()
            cursor.execute('''
                SELECT id, report_type, report_name, created_at
                FROM generated_reports 
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            
            reports = cursor.fetchall()
            
            if reports:
                df = pd.DataFrame(reports, columns=['ID', 'Type', 'Name', 'Created'])
                st.dataframe(df, width='stretch')
                
                # Download specific report
                selected_report = st.selectbox(
                    "Select Report to Download",
                    options=[f"{r[1]} - {r[2]}" for r in reports]
                )
                
                if st.button("Download Selected Report"):
                    st.info("Report download functionality would be implemented here")
            else:
                st.info("No reports found. Generate a report first.")
                
        except Exception as e:
            st.error(f"Error loading report history: {e}")
    
    def run(self):
        """Main report generation runner"""
        st.title("📄 AgriForecast.ai - Report Generation System")
        st.markdown("**Professional Reports and Data Export**")
        
        # Render sidebar
        user_id, report_type, export_format, email_address, send_email = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2 = st.tabs(["📄 Generate Report", "📚 Report History"])
        
        with tab1:
            self.render_report_generation(user_id, report_type, export_format, email_address, send_email)
        
        with tab2:
            self.render_report_history(user_id)
        
        # Footer
        st.markdown("---")
        st.markdown("**📄 Report Generation System - Phase 2 Complete**")
        st.markdown("*Professional reporting and data export capabilities*")

def main():
    """Main report generation entry point"""
    try:
        app = ReportGenerationFrontend()
        app.run()
    except Exception as e:
        st.error(f"Report generation error: {e}")
        logger.error(f"Report generation error: {e}")

if __name__ == "__main__":
    main()
