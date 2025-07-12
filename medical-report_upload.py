from google.cloud import storage
import os

# --- Step 1: Your Service Account Credential ---
service_account_info = {
    "type": "service_account",
    "project_id": "twilio-440407",
    "private_key_id": "9049c36e31b5fab27365f3bf8659d1a4184012aa",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDVEIUHhDupAv7y\nAOOj7z9p0myhBoMsUnLvsdxoMjc2AP1t1kPcBV+tZMNMfP4x/OpESHC2z+pB95ye\nhIVfZQIZblH3x8nVyOak/We54KO0fp1WkJWZ4gMOxr2MQZxwGc2EbcTcgjDDHJ/q\nHFcam/ziXq2BJFO+CUiNXXFSEbVlnca6JQCeNHcpJAddfEw5+45dEawoZyU593rU\nIV/32TuXacruzLj9ws6cR3ACV2zEDcU+0j1X3X5KmHBt9S6Fi6sBDWoJK5YcH0Qq\nBQN3zEUcO7QmQrQ8z1Srt8Bwrdm1pSDfpaHdoDpF79dJUJQ2sQzZseo/kPiOLavJ\no1OE5909AgMBAAECggEAKhvG8s6ZPOSc7saqtrxCr98YvXVMSN7tnL4t1YDxJPDq\npUHGrQ351Aq5R11fnpEB2qdncVXjkhCGCVUfB9SuZsjFFd+MHf6DyOFVFekV6Ybp\ngRF3o49Fs+6myPixmn0a/zxzfvITAYifeTULKPThtHpqN37utvzeNCQe0I2z6EY7\nPxCDiirXypvJWFOnTslLQU3G2+8xmetKZlgpCv3Z7CYWr4x1BZ7gahf1rP1lsg8c\nnB442qZft1/uE/bBfgRzl6ntuujjC7FuPi9u2R9Hp4D3yh5NAU+ewQmR8t7g/pv4\nLO8KqdX5maQq+SV/xjZP3luvW8sNHZC+Uv+9Ghtk4QKBgQDySJbUh/2tNZOwSogT\ndzZq1CLC1ehLJOt6mxUzLZ4ryIPAMDpU+qg3fArpj8XhEjDzfycegf9N6H1UQwXw\nKRYWXjo/F3QDoS26744en37EtuOo3Ntq1XeoQo2uVsNFLn23RSsAmxFAYkOH2O0L\n229kFTXnxJ2ETyUdCfPaRon8IQKBgQDhIHWyPg/4rnqf1hfKe9Tx6cVRYVuQ3acm\nKfIr6EzXjCHtjw8irsETCucXS69A7MzmekCh9BGy8LoAREbEtnCtPvoi6HR01hR3\ngwSWfunWI+tvYSOrJhiWag6m8SjY5R31kg4Mq3uSvSuyo0du9tqfifRb3hQm6KYU\nxlXIjaidnQKBgFj4MvsEnTD31a4NEH8lbcQ49jLZ3h2KBzbUsCpE/CpTzZ3LmAAQ\ns6j8Uf2GoEGQLo2cCb94OUpgr3U7z3hrfgLkwzrb3+xdSa+1vFiedSzDhEJEKAbJ\nMNGG7wQwNDC5a8zbB3mHeAROkUHXdOS/xd3YtBzR5I3rilNpjjR/ZrhBAoGBAKFB\nHez5lXkciUs6EDqCbqqFN0gug2cFzbeBbizTLU9r2dWOllnScQvR0GuYU8UemTox\nsWAQMilJUwHj5gj7YURHCua8OMaDnY9pcnzWFWrEudxC6UirdgsvlqUvsoGBw+7l\nmliq8E3QYJ+JYx5xhXGnYDf5n9eq52OUGVgZWADlAoGBAJ8USZEdn1NU7+f5z2b5\nAU0ctdFeK8vt8JSc3ECipt7k9l+ftlokujcISXt2x45kLxfo/sU/YNr+A1UpPL3E\nW9RAuX6vekAIo44wVGoGaVueoV4AI4S+CGmDAg7oYTpN8WueSxJZBccbLutjHf03\nHdmylb2zCoCb8jrZyLauATPv\n-----END PRIVATE KEY-----\n",
    "client_email": "global-access-sa@twilio-440407.iam.gserviceaccount.com",
    "client_id": "106229784886769538524",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/global-access-sa%40twilio-440407.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# --- Step 2: Upload function ---
def upload_lab_files_to_gcs(
    pdf_path: str,
    txt_path: str,
    filename: str,
    country_code: str,
    phone_number: str,
    service_account_info: dict
):
    try:
        # 1. Authenticate client
        client = storage.Client.from_service_account_info(service_account_info)
        bucket = client.bucket("medical_lab_data")

        # 2. Check both files exist
        if not os.path.exists(pdf_path):
            return {"status": "error", "message": f"Missing PDF file: {pdf_path}"}
        if not os.path.exists(txt_path):
            return {"status": "error", "message": f"Missing TXT file: {txt_path}"}

        # 3. Upload PDF and make it public
        pdf_blob_path = f"pdf_file/{country_code}/{phone_number}/{filename}.pdf"
        pdf_blob = bucket.blob(pdf_blob_path)
        pdf_blob.upload_from_filename(pdf_path)
        pdf_blob.make_public()

        # 4. Upload TXT (private)
        txt_blob_path = f"text_file/{country_code}/{phone_number}/{filename}.txt"
        txt_blob = bucket.blob(txt_blob_path)
        txt_blob.upload_from_filename(txt_path)

        # 5. Return result
        return {
            "status": "success",
            "message": "Files uploaded successfully. PDF is public.",
            "pdf_url": pdf_blob.public_url
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}



result = upload_lab_files_to_gcs(
    pdf_path="/content/RAJAN_SINGH_LIVER_REPORT_22-06-2025_2050.pdf",
    txt_path="/content/RAJAN_SINGH_LIVER_REPORT_22-06-2025_2050.txt",
    filename="RAJAN_SINGH_LIVER_REPORT_22-06-2025_2050",
    country_code="+91",
    phone_number="8319637167",
    service_account_info=service_account_info
)

print(result)



result = upload_lab_files_to_gcs(
    pdf_path="/content/NAINA_SINGH_BLOOD_REPORT_22-06-2025_2024.pdf",
    txt_path="/content/NAINA_SINGH_BLOOD_REPORT_22-06-2025_2024.txt",
    filename="NAINA_SINGH_BLOOD_REPORT_22-06-2025_2024",
    country_code="+91",
    phone_number="8319637167",
    service_account_info=service_account_info
)

print(result)
