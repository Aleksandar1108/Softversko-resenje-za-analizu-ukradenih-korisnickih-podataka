"""Email notification service."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict

from ...config.settings import settings


class EmailService:
    """Service for sending email notifications."""
    
    def __init__(self):
        """Initialize email service."""
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or self.smtp_user
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: str = None,
    ) -> bool:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            
        Returns:
            True if email was sent successfully
        """
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email
            
            # Add plain text part
            text_part = MIMEText(body, "plain")
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, "html")
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_breach_alert(
        self,
        to_email: str,
        breach_name: str,
        breach_details: Dict,
    ) -> bool:
        """
        Send breach alert email.
        
        Args:
            to_email: Recipient email address
            breach_name: Name of the breach
            breach_details: Additional breach details
            
        Returns:
            True if email was sent successfully
        """
        subject = f"Security Alert: Your email found in {breach_name} breach"
        
        body = f"""
Dear User,

We have detected that your email address was found in the following data breach:

Breach Name: {breach_name}

We recommend that you:
1. Change your password immediately if you haven't already
2. Enable two-factor authentication if available
3. Use a unique, strong password for this account
4. Check other accounts that might use the same password

For more information and recommendations, please visit our dashboard.

Best regards,
Breach Analyzer Team
"""
        
        html_body = f"""
<html>
<body>
<h2>Security Alert</h2>
<p>Your email address was found in the following data breach:</p>
<p><strong>Breach Name:</strong> {breach_name}</p>
<h3>Recommended Actions:</h3>
<ul>
<li>Change your password immediately</li>
<li>Enable two-factor authentication</li>
<li>Use a unique, strong password</li>
<li>Check other accounts with the same password</li>
</ul>
</body>
</html>
"""
        
        return await self.send_email(to_email, subject, body, html_body)
