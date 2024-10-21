from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import format_html

def send_attendee_welcome_email(attendee):
    subject = 'Thank You for Registering for Hacktoberfest 2024!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [attendee.email]

    # Email content (HTML format)
    html_message = format_html(
        f"""
        <p>Hey {attendee.name},</p>
        <p>
            Thank you for registering for Hacktoberfest 2024, organized by amFOSS in association with GitHub. 
            We're thrilled to have you join us for this one-day event where you'll make your first contribution 
            to open source and attend lightning talks from industry experts.
        </p>
        <p>
            We are delighted to have had a huge number of applicants this year and are excited to celebrate 
            this joyous occasion with you.
        </p>

        <h3>Details:</h3>
        <p><strong>Event:</strong> amFOSS Hacktoberfest</p>
        <p><strong>Date:</strong> 22nd October 2024</p>
        <p><strong>Time:</strong> 9:00 AM - 6:00 PM</p>
        <p><strong>Venue:</strong> Amriteshwari Hall</p>

        <p>
            To maximize the event's benefits, we urge you to bring your laptop along with your charger. Without it, 
            you will be unable to work together and send PRs. Although you can attend the talks and share laptops, 
            you will need to send PRs individually to compete in games and make contributions to win GitHub swag 
            and other prizes.
        </p>

        <p>
            Also, make sure you install 
            <a href="https://git-scm.com/downloads">Git Bash</a> and create a 
            <a href="https://github.com/">GitHub</a> account as you will need them to use the terminal commands 
            and contribute. You don't have to install Git Bash if you are using Linux or macOS.
        </p>

        <p>
            <strong>Important</strong>: Please ensure that you have the <strong>QR code</strong> attached to this email ready at the entrance for check-in. Without it, you won’t be able to enter the venue.
        </p>

        <p>
            So, are you ready? As the last step, RSVP for the event at the link given below to confirm your participation. 
            We look forward to your presence at the event!
        </p>

        <p><strong>Link:</strong> <a href="https://events.mlh.io/events/11765-amfoss-hacktoberfest-24">RSVP for Hacktoberfest</a></p>

        <p>
            If you face any technical issues, feel free to reach out to us at:<br><br>
            <a href="tel:+919497547035">WhatsApp</a> | <a href="http://t.me/Viserion_7">Telegram</a>
            <br>Harigovind C B<br>
            Organizer
        </p>
        """
    )

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'

    if attendee.qr_code:
        qr_code_path = attendee.qr_code.path
        with open(qr_code_path, 'rb') as qr_code_file:
            email.attach('qr_code.png', qr_code_file.read(), 'image/png')

    email.send()
