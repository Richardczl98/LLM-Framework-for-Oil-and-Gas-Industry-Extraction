# Get the samples from http://www.adobe.com/go/pdftoolsapi_python_sample
# Run the sample:
# python src/extractpdf/extract_txt_table_info_from_pdf.py
# need 'pip install pdfservices-sdk==4.0.0'
import os
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job import ExtractPDFJob
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_pdf_params import ExtractPDFParams
from adobe.pdfservices.operation.pdfjobs.result.extract_pdf_result import ExtractPDFResult

import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# change to your adobe client_id and client_secret
CLIENT_ID = 'cf0dc8a3bd3248d2949aced56bfd7821'
CLIENT_SECRET = 'p8e-C2PYx8q8T1jE2Y1tsdcKsseCS8jn2P7x'


class ExtractTextInfoFromPDF:
    def __init__(self,
                 pdf_file_path: str,
                 save_zip_path: str,
                 with_tabels=False):
        if not os.path.exists(pdf_file_path):
            raise Exception(f'PDF file not found: {pdf_file_path}')
        with open(pdf_file_path, 'rb') as f:
            input_stream = f.read()
        try:
            credentials = ServicePrincipalCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)

            # Create parameters for the job
            if with_tabels:
                extract_pdf_params = ExtractPDFParams(
                    elements_to_extract=[ExtractElementType.TEXT, ExtractElementType.TABLES],
                )
            else:
                extract_pdf_params = ExtractPDFParams(
                    elements_to_extract=[ExtractElementType.TEXT],
                )

            # Creates a new job instance
            extract_pdf_job = ExtractPDFJob(input_asset=input_asset, extract_pdf_params=extract_pdf_params)

            # Submit the job and gets the job result
            location = pdf_services.submit(extract_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, ExtractPDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_resource()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)
            with open(save_zip_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')


def pdf_text_tabel_to_zip(pdf_path: str,
                          save_zip_path=None,
                          with_tabels=True):
    """
    Only extract pdf text
    :param pdf_path:
    :param save_zip_path:
    :return: A zip file. Only contains a json file.
    """
    if not os.path.exists(pdf_path):
        raise Exception(f'PDF file not found: {pdf_path}')
    if not save_zip_path:
        save_zip_path = pdf_path.replace(".pdf", ".zip")
    if os.path.isfile(save_zip_path):
        os.remove(save_zip_path)
    ExtractTextInfoFromPDF(pdf_file_path=pdf_path, save_zip_path=save_zip_path, with_tabels=with_tabels)



if __name__ == '__main__':
    pdf_text_tabel_to_zip("../data/spe/spe-179612-ms.pdf",
                          "../spe-179612-ms.zip")
