import csv
from reportlab.lib.pagesizes import letter
import reportlab.pdfgen.canvas as canvas
from reportlab.lib.units import inch
import configparser


import constants
import render


def main():
    config = configparser.ConfigParser()
    config.read(constants.PROPERTIES_FILE, encoding="utf-8")

    COMPANY = config.get(constants.SECTION, constants.COMPANY_KEY)
    COMPANY_ADRESS = config.get(constants.SECTION, constants.COMPANY_ADRESS_KEY)
    COMPANY_POSTAL_CODE = config.get(
        constants.SECTION, constants.COMPANY_POSTAL_CODE_KEY
    )
    COMPANY_CITY = config.get(constants.SECTION, constants.COMPANY_CITY_KEY)
    COMPANY_PHONE_NUMBER = config.get(constants.SECTION, constants.PHONE_NUMBER_KEY)
    CEO = config.get(constants.SECTION, constants.CEO_KEY)
    BANK = config.get(constants.SECTION, constants.BANK_KEY)
    ACCOUNT_NUMBER = config.get(constants.SECTION, constants.ACCOUNT_NUMBER_KEY)
    COMPANY_ORGANIZATION_NUMBER = config.get(
        constants.SECTION, constants.COMPANY_ORGANIZATION_NUMBER_KEY
    )
    EMAIL = config.get(constants.SECTION, constants.EMAIL_KEY)
    IBAN = config.get(constants.SECTION, constants.IBAN_KEY)
    BIC = config.get(constants.SECTION, constants.BIC_KEY)
    current_invoice_number = config.get(constants.SECTION, constants.INVOICE_NUMBER_KEY)
    CLIENT_NUMBER = config.get(constants.SECTION, constants.CLIENT_NUMBER_KEY)
    CLIENT_REFERENCE = config.get(constants.SECTION, constants.CLIENT_REFERENCE_KEY)
    CLIENT_ORGANIZATION_NUMBER = config.get(
        constants.SECTION, constants.CLIENT_ORGANIZATION_NUMBER_KEY
    )
    PAYMENT_DAYS = config.getint(constants.SECTION, constants.PAYMENT_DAYS_KEY)

    CLIENT = config.get(constants.SECTION, constants.CLIENT_KEY)
    CLIENT_ADRESS = config.get(constants.SECTION, constants.CLIENT_ADRESS_KEY)
    CLIENT_POSTAL_CODE = config.get(constants.SECTION, constants.CLIENT_POSTAL_CODE_KEY)
    CLIENT_CITY = config.get(constants.SECTION, constants.CLIENT_CITY_KEY)

    # print(COMPANY, ADRESS, POSTAL_CODE, CITY, PHONE_NUMBER)

    # Set up the PDF file
    c = canvas.Canvas("invoice.pdf", pagesize=letter)

    # Set up the font and font size
    c.setFont("Helvetica", 12)

    # Read the CSV file
    with open("sample_invoice_data.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=["Tjänst", "Beskrivning", "Antal", "Á-pris", "Belopp"],
            delimiter=";",
        )
        data = [row for row in reader]

    # Remove the header
    data = data[1:]

    invoice_total = sum(float(row["Belopp"]) for row in data)

    # Create the invoice header
    render.drawCentredText(c, "Faktura", constants.WIDHT / 2, 10 * inch, 24)

    render.drawCompanyInformation(
        c,
        COMPANY,
        COMPANY_ADRESS,
        COMPANY_POSTAL_CODE,
        COMPANY_CITY,
        COMPANY_PHONE_NUMBER,
    )

    render.drawClientInformation(
        c, CLIENT, CLIENT_ADRESS, CLIENT_POSTAL_CODE, CLIENT_CITY
    )

    render.drawPaymentInformation(
        c,
        invoice_total,
        COMPANY,
        COMPANY_ADRESS,
        CEO,
        BANK,
        COMPANY_POSTAL_CODE,
        COMPANY_CITY,
        COMPANY_PHONE_NUMBER,
        ACCOUNT_NUMBER,
        COMPANY_ORGANIZATION_NUMBER,
        EMAIL,
        IBAN,
        BIC,
        current_invoice_number,
        CLIENT_NUMBER,
        CLIENT_REFERENCE,
        CLIENT_ORGANIZATION_NUMBER,
        PAYMENT_DAYS,
    )

    render.drawInvoiceItems(c, data)

    # Save the PDF file
    c.save()


if __name__ == "__main__":
    main()
