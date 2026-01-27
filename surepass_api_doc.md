# Surepass API Docs

# Surepass API

## Introduction

The API is built using RESTful endpoints and standard HTTP verbs.

-   Response codes are used to indicate the status of the message and any error codes.
    
-   JSON is returned on all our API responses, including errors, with a consistent structure for all messages.
    
-   Authentication to the API is performed via token-based auth.
    
-   Requests to our API should be made as JSON, except when uploading documents.
    
-   All API requests must be made over HTTPS. Calls made over plain HTTP will fail.
    
-   All requests must use TLS 1.2 or above, with Server Name Indication enabled
    
-   Text fields support UTF-8, but do not allow certain special characters that could be used maliciously.
    

# Getting Started

Surepass' API exposes the entire Surepass infrastructure via a standardized programmatic interface. Using Surepass' API, you can avail all of our services, while using your programming language of choice. The Surepass API is a RESTful API based on HTTP requests and JSON responses.

This version of the API, version 1. All requests work on HTTPS.

The easiest way to start using the Surepass API is by clicking the **Run in Postman** button above. [Postman](https://www.getpostman.com/) is a free tool which helps developers run and debug API requests, and is the source of truth for this documentation. Every endpoint you see documented here is readily available by running our Postman collection.

## Need help?

The Surepass engineers are always around answering questions. The quickest way to get help is by contacting us at [techsupport@surepass.io](https://mailto:techsupport@surepass.io)

All the resources require Token Authentication. So all requests have to be provided with an authorization header along with the token

Plain Text

```plain
Authorization: Bearer <YOUR_TOKEN>
```

### Registration Quickstart

To get a token for staging and then subsequently for production contact us at - [techsupport@surepass.io](https://mailto:techsupport@surepass.io)

## Trial Usage

The Aadhaar API provides a trial for 3 days with a usage limit of 50 requests. Contact us at [techsupport@surepass.io](https://mailto:techsupport@surepass.io) to start your trial.

# Endpoints

The API is accessed by making HTTP requests to a specific version endpoint URL, in which GET or POST variables contain information about what you wish to access. Every endpoint is accessed via an SSL-enabled HTTPS.

Everything (methods, parameters, etc.) is fixed to a version number, and every call must contain one. Different Versions are available at different endpoint URLs. The latest version is Version 1.

The stable HTTP endpoint for the latest version are:

**Production**

bash

```bash
https://kyc-api.surepass.io/api/v1
```

**Sandbox**

bash

```bash
https://sandbox.surepass.io/api/v1
```

## Responses

Each response is wrapped in a data tag. This means if you have a response, it will always be within the data field. We also include a status code, success flag, type and message in the responseof each request.

View More

json

```json
{
    "data": {
        "pan_number": "AAAPM1234L",
        "full_name": "MUNNA BHAIYA",
        "father_name": "KALEEN BHAIYA",
        "client_id": "takdTqhCxo",
        "dob": "1990-01-01"
},
    "status_code": 200,
    "message": "",
    "success": true
}
```

# Authentication

The API uses token-based authentication. You will be provided with a token which must be included in the header of all requests made to the API.

All API requests must be made over HTTPS. Any requests made over HTTP will fail.

You will be provided with both live and sandbox tokens. Requests made with the sandbox token can be used to test our API before going live. Requests made in sandbox-mode will return actual responses and trial credits capped at 50 will be deducted from your account.

Plain Text

```plain
Authorization: Bearer <YOUR_TOKEN>
```

# Errors and Status Codes

Standard HTTP error codes are returned in the case of a failure. 2xx codes indicate a successful message; 4xx codes indicate an error caused by information provided by the client; and 5xx codes indicate an error on Surepass' servers.

## Status Codes

Status Codes

Name

Meaning

200

OK

Successful Request.

201

Created

Resource successfully created.

202

Accepted

Asynchronous Request. Response will be sent to configured Webhook.

204

No Content

Successful with no Response.

## Error Codes

Error Code

Name

Meaning

400

Bad Request

Malformed request

401

Unauthorized

Invalid authorization credentials

403

Forbidden

Action prohibited

404

Not Found

Resource not found

422

Unprocessable Entity

Validation error

429

Too Many Requests

Rate limit reached

500

Internal Server Error

An unexpected error occurred in our API

# Rate Limits

Surepass' API enforces a maximum volume of requests per minute for all clients. Unless contractually agreed otherwise, the maximum rate is 100 requests per minute.

Any request over the limit will return a 429 HTTP response.

## Avoiding the limit

The tips below are some simple suggestions to help reduce the possibility of being rate limited. We recommend:

-   running non essential or routine batch API jobs outside your peak hours.
    
-   throttling batch jobs.
    
-   implementing an exponential back-off approach for requests essential to your verification process, with an initial delay of 30 seconds.
    
-   prioritising requests that are essential to verify an active user.
    
-   setting up monitors and alerts for error responses on our API.
    

## API Deprecation

When an API endpoint is scheduled for deprecation the following actions will be taken:

-   The endpoint documentation will be marked as deprececated and a migration plan will be added.
    
-   The endpoint will have a `Sunset` header ([Sunset HTTP Header](https://tools.ietf.org/id/draft-wilde-sunset-header-03.html)) added to incidate the last date the endpoint should be relied upon.
    
-   A email will be sent to active third party developers notifing of the deprecation.
    

When the `Sunset` date has passed followup email will be sent to active third party developers notifing of the deprecation.

## Backwards Compatibility

The following changes are considered backwards compatible:

-   Adding new API endpoints.
    
-   Adding new properties to the responses from existing API endpoints.
    
-   Adding optional request parameters to existing API endpoints.
    
-   Altering the format or length of IDs.
    
-   Altering the message attributes returned by validation failures or other errors.
    
-   Sending webhooks for new event types.
    
-   Reordering properties returned from existing API endpoints.
    

## Additional Information

If you have questions that aren't answered here, contact the Support Team - [techsupport@surepass.io](https://mailto:techsupport@surepass.io).

AUTHORIZATIONBearer Token

Token

TOKEN

## 

Voter ID

This API provides information About Voter ID, Including Full Name, Date Of Birth, Age, House No, State, District, Assembly Constituency, Assembly Constituency Number, Polling Station Name, etc.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

## 

PAN Udyam Check

This API allows users to check the Udyam registration status based on a PAN (Permanent Account Number) number.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### POSTPAN Udyam Check

https://kyc-api.surepass.io/api/v1/corporate/pan-udyam-check

**Request Body**

**Key**

**Format**

**Description**

pan\_number

String

Enter PAN Number As An Input

full\_name

String

Enter Full As An Input

dob

String

Enter Date Of Birth in "YYYY-MM-DD" Format

**Response Body**

**Key**

**Format**

**Description**

client\_id

String

Unique Client ID

pan\_number

String

PAN Number

udyam\_exists

Boolean

Udyam Exists Corresponding PAN Status

migration\_status

String Enum

Udyam Migration Status

`migration_status` can have the following values:

-   `migrated`
    
-   `not_migrated`
    

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "pan_number": "ABBCS1234D",
    "full_name": "SURJAL PRIVATE LIMITED",
    "dob": "2018-11-15"
}
```

Example Request

Migrated

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/corporate/pan-udyam-check' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "pan_number": "ABBCS1234D",
    "full_name": "SURJAL SERVICES PRIVATE LIMITED",
    "dob": "2018-11-15"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "pan_udyam_check_nlGIZduXrlnwWuYfbznH",
    "pan_number": "ABBCS1234D",
    "udyam_exists": true,
    "migration_status": "migrated"
  },
  "status_code": 200,
  "success": true,
  "message": null,
  "message_code": "success"
}
```

Date

Mon, 20 May 2024 13:09:40 GMT

Content-Type

application/json

Content-Length

227

Connection

keep-alive

### POSTInitialize NSDL

https://kyc-api.surepass.io/api/v1/esign/initialize

**Request Body**

Key

Format

Description

pdf\_pre\_uploaded

Boolean (Optional)

If PDF is being uploaded by merchant.

callback\_url

String (Optional)

Callback URL after eSign is complete.

config

Object

Config for eSign (see example).

**Notes**:

-   Auth Mode 1 - For Aadhaar OTP based eSign
    
-   Auth Mode 2 - For fingerprint based eSign
    
-   Auth Mode 3 - For Iris base eSign
    
-   Auth Mode 4 - For Face Match based eSign
    

**Response Body**

Key

Format

Description

client\_id

String

Unique identifier of this object/ query.

token

String

Token generated for use by SDK

url

String

URL generated for use by SDK/ Customer.

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

View More

json

```json
{
    "pdf_pre_uploaded": false,
    "callback_url": "https://example.com?state=test",
    "config": {
        "accept_selfie": true,
        "allow_selfie_upload": true,
        "accept_virtual_sign": true,
        "track_location": true,
        "auth_mode": "1",
        "reason": "Contract",
        "positions": {
            "1": [
                {
                    "x": 10,
                    "y": 20
                }
            ]
            
        }
    },
    "prefill_options": {
        "full_name": "Munna Bhaiya",
        "mobile_number": "9876543210",
        "user_email": "karankapoor229@gmail.com"
    }
}
```

Example Request

Initialize

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/esign/initialize' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data-raw '{
    "pdf_pre_uploaded": false,
    "callback_url": "https://example.com?state=test",
    "config": {
        "auth_mode": "1",
        "reason": "Contract",
        "positions": {
            "1": [
                {
                    "x": 10,
                    "y": 20
                }
            ],
            "2": [
                {
                    "x": 0,
                    "y": 0
                }
            ]
        }
    },
    "prefill_options": {
        "full_name": "Munna Bhaiya",
        "mobile_number": "9876543210",
        "user_email": "munna@gmail.com"
    }
}'
```

Example Response

-   Body
-   Headers (1)

View More

json

```json
{
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ababtjtjnbaesergrtjnnfeW32rfWAFF1tgWs.UtugjhGuy567hjJHFGyi-m3JJn4-o",
    "client_id": "esign_HLiwHZZxuUjZLqylzzvU",
    "url": "https://esign-client.aadhaarkyc.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ababtjtjnbaesergrtjnnfeW32rfWAFF1tgWs.UtugjhGuy567hjJHFGyi-m3JJn4-o"
  },
  "message_code": "success",
  "success": true,
  "message": "User initialized successfully",
  "status_code": 200
}
```

Content-Type

application/json

### POSTInitialize NSDL with Stamp

https://kyc-api.surepass.io/api/v1/esign/initialize

**Request Body**

Key

Format

Description

pdf\_pre\_uploaded

Boolean (Optional)

If PDF is being uploaded by merchant.

callback\_url

String (Optional)

Callback URL after eSign is complete.

config

Object

Config for eSign (see example).

**Notes**:

-   Auth Mode 1 - For Aadhaar OTP based eSign
    
-   Auth Mode 2 - For fingerprint based eSign
    
-   Auth Mode 3 - For Iris base eSign
    
-   Auth Mode 4 - For Face Match based eSign
    
-   You need to add the `stamp_paper_amount` and `stamp_paper_state` in the `config` object to request an Esign with Stamps.
    
-   Additionally you can add arbitrary data on the stamp paper using the `stamp_data` object.
    

**Response Body**

Key

Format

Description

client\_id

String

Unique identifier of this object/ query.

token

String

Token generated for use by SDK

url

String

URL generated for use by SDK/ Customer.

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

View More

json

```json
{
    "pdf_pre_uploaded": false,
    "callback_url": "https://example.com?state=test",
    "config": {
        "accept_selfie": true,
        "allow_selfie_upload": true,
        "accept_virtual_sign": true,
        "track_location": true,
        "auth_mode": "1",
        "reason": "Contract",
        "positions": {
            "1": [
                {
                    "x": 10,
                    "y": 20
                }
            ]
            
        },
        "stamp_paper_amount": 100,
        "stamp_paper_state": "Maharashtra",
        "stamp_data": {
            "Name": "John Doe",
            "DOB": "January 1, 1985",
            "Address": "123 Main Street, Springfield, IL, USA",
            "Passport Number": "X12345678",
            "Email": "john.doe@example.com",
            "Mobile": "+1 (123) 456-7890",
            "Mother's Name": "Jane Doe",
            "Father's Name": "James Doe",
            "Occupation": "Software Developer",
            "Work Address": "456 Elm Street, Springfield, IL, USA"
        }
    },
    "prefill_options": {
        "full_name": "Munna Bhaiya",
        "mobile_number": "9876543210",
        "user_email": "karankapoor229@gmail.com"
    }
}
```

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/esign/initialize' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data-raw '{
    "pdf_pre_uploaded": false,
    "callback_url": "https://example.com?state=test",
    "config": {
        "accept_selfie": true,
        "allow_selfie_upload": true,
        "accept_virtual_sign": true,
        "track_location": true,
        "auth_mode": "1",
        "reason": "Contract",
        "positions": {
            "1": [
                {
                    "x": 10,
                    "y": 20
                }
            ]
            
        },
        "stamp_paper_amount": 100,
        "stamp_paper_state": "Maharashtra",
        "stamp_data": {
            "Name": "John Doe",
            "DOB": "January 1, 1985",
            "Address": "123 Main Street, Springfield, IL, USA",
            "Passport Number": "X12345678",
            "Email": "john.doe@example.com",
            "Mobile": "+1 (123) 456-7890",
            "Mother'\''s Name": "Jane Doe",
            "Father'\''s Name": "James Doe",
            "Occupation": "Software Developer",
            "Work Address": "456 Elm Street, Springfield, IL, USA"
        }
    },
    "prefill_options": {
        "full_name": "Munna Bhaiya",
        "mobile_number": "9876543210",
        "user_email": "karankapoor229@gmail.com"
    }
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "esign_qXEdSjadoLIewCeTkcCa",
    "group_id": null,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjM1MzYwNCwianRpIjoiZmYwYzcyNzYtOTJjMi00ZjNmLTgwYjgtMGNhZjNiOTk0ODkxIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoiZXNpZ25fcVhFZFNqYWRvTElld0NlVGtjQ2EiLCJuYmYiOjE3MTIzNTM2MDQsImV4cCI6MTcxMjk1ODQwNCwidXNlcl9jbGFpbXMiOnsiZ2F0ZXdheSI6InNhbmRib3gifX0.vsI5Y-UQCKrxMqwECviORA_iSDqO4RMaaGGi5_IQ1L4",
    "url": "https://esign-client.surepass.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjM1MzYwNCwianRpIjoiZmYwYzcyNzYtOTJjMi00ZjNmLTgwYjgtMGNhZjNiOTk0ODkxIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoiZXNpZ25fcVhFZFNqYWRvTElld0NlVGtjQ2EiLCJuYmYiOjE3MTIzNTM2MDQsImV4cCI6MTcxMjk1ODQwNCwidXNlcl9jbGFpbXMiOnsiZ2F0ZXdheSI6InNhbmRib3gifX0.vsI5Y-UQCKrxMqwECviORA_iSDqO4RMaaGGi5_IQ1L4"
  },
  "status_code": 200,
  "message_code": "success",
  "message": "User initialized successfully",
  "success": true
}
```

Date

Fri, 05 Apr 2024 21:46:44 GMT

Content-Type

application/json

Content-Length

948

Connection

keep-alive

### POSTUpload PDF

{{upload\_url}}

Pass the parameters as received in previous Get Upload Link Response

Bodyformdata

x-amz-signature

{{signature}}

x-amz-date

{{date}}

x-amz-credential

{{credentials}}

key

{{upload\_key}}

policy

{{policy}}

x-amz-algorithm

{{algorithm}}

file

Example Request

Upload PDF

curl

```curl
curl --location -g '{{upload_url}}' \
--form 'x-amz-signature="{{signature}}"' \
--form 'x-amz-date="{{date}}"' \
--form 'x-amz-credential="{{credentials}}"' \
--form 'key="{{upload_key}}"' \
--form 'policy="{{policy}}"' \
--form 'x-amz-algorithm="{{algorithm}}"' \
--form 'file=@"/C:/Users/karan/Desktop/ASP Audit Checklist v1.2.pdf"'
```

Example Response

-   Body
-   Headers (0)

No response body

This request doesn't return any response body

No response headers

This request doesn't return any response headers

### POSTUpload PDF via Link

https://kyc-api.surepass.io/api/v1/esign/upload-pdf

Endpoint to pre-upload eSign PDF via an URL.

**Request URL Parameters**

Key

Format

Description

client\_id

String

Unique Client ID

link

String

URL of the PDF

**Response Body**

Key

Format

Description

uploaded

Boolean

File uploaded successfully or not

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "client_id": "{{client_id}}",
    "link": "https://www.aeee.in/wp-content/uploads/2020/08/Sample-pdf.pdf"
}
```

Example Request

Success

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/esign/upload-pdf' \
--header 'Content-Type: application/json' \
--data '{
    "client_id": "{{client_id}}",
    "link": "https://www.aeee.in/wp-content/uploads/2020/08/Sample-pdf.pdf"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

json

```json
{
  "data": {
    "uploaded": true
  },
  "status_code": 200,
  "message_code": "success",
  "message": "Success",
  "success": true
}
```

Date

Fri, 03 May 2024 14:31:13 GMT

Content-Type

application/json

Content-Length

115

Connection

keep-alive

### POSTCredit Report Cibil PDF

https://kyc-api.surepass.io/api/v1/credit-report-cibil/fetch-report-pdf

This API provides access to a CIBIL credit report(Hard Pull) in PDF format for a specified client. The response includes basic client details such as name, mobile number, PAN, credit score, and a URL to download the PDF version of the credit report.

**Request Body**

**Key**

**Format**

**Description**

mobile

String

Enter Mobile Number

pan

String

Enter PAN Number

name

String

Enter Full Name

gender

String Enum

Enter Gender

consent

String Enum

User Consent

`gender` can have the following values:

-   `male`
    
-   `female`
    

`consent` can have the following values:

-   `Y`

**Response Body**

Key

Format

Description

client\_id

String

Unique Client ID

mobile

String

Mobile Number

pan

String

PAN Number

name

String

Full Name

gender

String

Gender

credit\_score

String

Credit Score

credit\_report

Object

Credit Report(as received from the bureau)

credit\_report\_link

String

Credit Report PDF LInk

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "mobile": "9988776655",
    "pan": "EKRPR1234F",
    "name": "Vishal Rathore",
    "gender": "male",
    "consent": "Y"
}
```

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/credit-report-cibil/fetch-report-pdf' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "mobile": "9966887744",
    "pan": "EKRPR1234F",
    "name": "Vishal Rathore",
    "gender": "male",
    "consent": "Y"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "credit_report_cibil_pdf_vIaturrIyayNxedOUOsG",
    "name": "Vishal Rathore",
    "mobile": "9966887744",
    "pan": "EKRPR1234F",
    "gender": "male",
    "credit_score": "744",
    "credit_report": {},
    "credit_report_link": "https://aadhaar-kyc-docs.s3.amazonaws.com/vishal.rathore.surepass/credit_report_cibil/credit_report_cibil_pdf_vIaturrIyayNxedOUOsG/credit_report_1726650832704638.pdf?X-Amz-Algorithm=AWS4-HMAC-S5"
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Wed, 18 Sep 2024 09:13:52 GMT

Content-Type

application/json

Content-Length

749

Connection

keep-alive

## 

Commercial

This contains APIs for retrieving business commercial credit reports in JSON and PDF formats.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### POSTCredit Report Commercial

https://kyc-api.surepass.io/api/v1/credit-report-commercial/fetch-report

This API provides access to a commercial credit report in JSON format for a specified business. The response includes business details such as business\_name, mobile number, PAN, credit score, and credit report.

**Request Body**

**Key**

**Format**

**Description**

business\_name

String

Enter Business Name

pan

String

Enter PAN Number

mobile

String

Enter Mobile Number

consent

String

User Consent

`consent` can have the following values:

-   `Y`

**Response Body**

Key

Format

Description

client\_id

String

Unique Client ID

pan

String

PAN Number

mobile

String

Mobile Number

business\_name

String

Business Name

credit\_score

String

Credit Score

credit\_report

Object

Credit Report(as received from the bureau)

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "business_name": "SHAIK SADIQ ALI",
    "mobile": "8977715735",
    "pan": "IQGPS3724B",
    "consent": "Y"
}
```

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/credit-report-commercial/fetch-report' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "business_name": "SHAIK SADIQ ALI",
    "mobile": "8977715735",
    "pan": "IQGPS3724B",
    "consent": "Y"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```
{
  "data": {
    "client_id": "credit_report_commercial_blcqfwxnzjVYtpHDHpes",
    "pan": "IQGPS3724B",
    "mobile": "8977715735",
    "business_name": "SHAIK SADIQ ALI",
    "credit_score": "",
    "credit_report": {
      "credit_report_s3_key": "",
      "credit_report": {
        "InquiryResponseHeader": {
          "ClientID": "027BB02400",
          "CustRefField": "1234",
          "ReportOrderNO": "16954344",
          "ProductCode": [
            "CCR"
          ],
          "SuccessCode": "1",
          "Date": "2025-02-26",
          "Time": "12:11:49"
        },
        "CommercialRequestInfo": {
          "InquiryPurpose": "9002",
          "TransactionAmount": "100",
          "BusinessName": "SHAIK SADIQ ALI",
          "InquiryAddresses": [
            {
              "seq": "1",
              "AddressType": [
                "O"
              ],
              "AddressLine1": "H NO1-11-28 PHULONG NIZAMABAD",
              "Locality": "ARMOOR",
              "City": "ARMOOR",
              "State": "MH",
              "Postal": "503001"
            }
          ],
          "InquiryPhones": [
            {
              "seq": "2",
              "PhoneType": [
                "M"
              ],
              "Number": "8977715735"
            }
          ],
          "EmailAddresses": [
            {
              "seq": "1",
              "EmailType": [
                ""
              ],
              "Email": "test1@equifax.com"
            },
            {
              "seq": "2",
              "EmailType": [
                ""
              ],
              "Email": "test2@equifax.com"
            }
          ],
          "IDDetails": [
            {
              "seq": "1",
              "IDType": "T",
              "IDValue": "IQGPS3724B",
              "Source": "Inquiry"
            }
          ],
          "CustomFields": [
            {
              "key": "ProductCategory",
              "value": "OnlyCBR"
            }
          ]
        },
        "Score": [
          {
            "Type": "ERS",
            "Version": "4.0"
          }
        ],
        "CCRResponse": {
          "Status": "1",
          "CommercialBureauResponse": {
            "Status": "1",
            "hit_as_borrower": "11",
            "hit_as_guarantor": "00",
            "InquiryResponseHeader": {
              "ClientID": "027BB02400",
              "CustRefField": "1234",
              "ReportOrderNO": "16954344",
              "TranID": "16954344",
              "ProductCode": [
                "CCR"
              ],
              "SuccessCode": "1",
              "Date": "2025-02-26",
              "Time": "12:11:49"
            },
            "InquiryRequestInfoCommercial": {
              "InquiryPurpose": "9002",
              "TransactionAmount": "100",
              "BusinessName": "SHAIK SADIQ ALI",
              "InquiryAddresses": [
                {
                  "seq": "1",
                  "AddressType": [
                    "Office"
                  ],
                  "AddressLine1": "H NO1-11-28 PHULONG NIZAMABAD",
                  "Locality": "ARMOOR",
                  "City": "ARMOOR",
                  "State": "MH",
                  "Postal": "503001"
                }
              ],
              "InquiryPhones": [
                {
                  "seq": "2",
                  "PhoneType": [
                    "M"
                  ],
                  "Number": "8977715735"
                }
              ],
              "EmailAddresses": [
                {
                  "seq": "1",
                  "EmailType": [
                    ""
                  ],
                  "Email": "test1@equifax.com"
                },
                {
                  "seq": "2",
                  "EmailType": [
                    ""
                  ],
                  "Email": "test2@equifax.com"
                }
              ],
              "IDDetails": [
                {
                  "seq": "1",
                  "IDType": "T",
                  "IDValue": "IQGPS3724B",
                  "Source": "Inquiry"
                }
              ],
              "CustomFields": [
                {
                  "key": "ProductCategory",
                  "value": "OnlyCBR"
                }
              ]
            },
            "CommercialBureauResponseDetails": {
              "IDAndContactInfo": {
                "CommercialPersonalInfo": {
                  "BusinessName": "SHAIK SADIQ ALI",
                  "BusinessLegalConstitution": "Not classified",
                  "BusinessCategory": "Others",
                  "BusinessIndustryType": "Others",
                  "ClassActivity": "52102",
                  "roc_BusinessLegalConstitution": false,
                  "roc_ClassActivity": false
                },
                "CommercialIdentityInfo": {
                  "PANId": [
                    {
                      "IdNumber": "IQGPS3724B"
                    }
                  ],
                  "roc_CIN": false,
                  "Dunsnbr": [
                    {
                      "seq": "1",
                      "IdNumber": "999999999"
                    }
                  ]
                },
                "CommercialAddressInfo": [
                  {
                    "Seq": "0",
                    "ReportedDate": "2020-03-31",
                    "Address": " H NO1-11-28 PHULONG NIZAMABAD NIZAMABAD",
                    "State": "Telangana",
                    "Postal": "503001",
                    "Type": "Registered Office",
                    "City": "ARMOOR",
                    "District": "Nizamabad",
                    "Country": "India"
                  }
                ],
                "CommercialPhoneInfo": [
                  {
                    "typeCode": "M",
                    "Number": "8977715735"
                  }
                ]
              },
              "CommercialCIRSummary": {
                "CommercialHeaderDetails": {
                  "member_name": "ICICI BANK LIMITED",
                  "last_updated_on": "31-03-2020"
                },
                "SeverityGrid": {
                  "SeverityGridDetailsMap": {
                    "2022-2023": {},
                    "2023-2024": {},
                    "2024-2025": {}
                  }
                },
                "EquifaxScoresCommercial": {
                  "CommercialScoreDetailsLst": [
                    {
                      "ScoreName": "Equifax Commercial Rank",
                      "ScoredEntity": "SHAIK SADIQ ALI",
                      "Relationship": "Borrower",
                      "ScoreValue": "7"
                    }
                  ]
                },
                "OverallCreditSummary": {
                  "AsBorrower": {
                    "2022-2023": {
                      "CF_Count": 1,
                      "OpenCF_Count": 1,
                      "Lenders_Count": 1,
                      "SanctionedAmtOpenCF_Sum": 200000,
                      "CurrentBalanceOpenCF_Sum": 32443
                    },
                    "2023-2024": {
                      "CF_Count": 1,
                      "OpenCF_Count": 1,
                      "Lenders_Count": 1,
                      "SanctionedAmtOpenCF_Sum": 200000,
                      "CurrentBalanceOpenCF_Sum": 32443
                    },
                    "2024-2025": {
                      "CF_Count": 1,
                      "OpenCF_Count": 1,
                      "Lenders_Count": 1,
                      "SanctionedAmtOpenCF_Sum": 200000,
                      "CurrentBalanceOpenCF_Sum": 32443
                    }
                  },
                  "AsGuarantor": {
                    "2022-2023": {},
                    "2023-2024": {},
                    "2024-2025": {}
                  }
                },
                "OpenCreditFacilitySummary": {
                  "AsBorrower": {
                    "Off-Member PSU Bank": {
                      "OpenCF_Count": 1,
                      "SanctionedAmount_Sum": 200000,
                      "CurrentBalance_Sum": 32443,
                      "OverdueAmount_Sum": 0
                    }
                  },
                  "AsGuarantor": {}
                },
                "DelinquencySummary": {
                  "AsBorrower": {},
                  "AsGuarantor": {},
                  "ForGuarantorRelatedEntitiesIndividuals": {}
                },
                "DerogSummary": {},
                "CreditTypeSummary": {
                  "AsBorrowerOnMember": {
                    "STD": {
                      "DPD 0": {},
                      "DPD 1-30": {},
                      "DPD 31-60": {},
                      "DPD 61-90": {},
                      "SMA 0": {},
                      "SMA 1": {},
                      "SMA 2": {},
                      "OVERDUE": {}
                    },
                    "NONSTD": {
                      "DPD 91-180": {},
                      "DPD > 180": {},
                      "SUB": {},
                      "RES": {},
                      "NPA": {},
                      "DBT": {},
                      "LOSS": {}
                    },
                    "CLOSED": {
                      "CLOSED": {}
                    },
                    "OTHERS": {
                      "OTHERS": {}
                    }
                  },
                  "AsBorrowerOffMember": {
                    "STD": {
                      "DPD 0": {
                        "TL_CFCount": 1,
                        "Total_CFCount": 1,
                        "TL_Amt": 32443,
                        "Total_Amt": 32443
                      },
                      "DPD 1-30": {},
                      "DPD 31-60": {},
                      "DPD 61-90": {},
                      "SMA 0": {},
                      "SMA 1": {},
                      "SMA 2": {},
                      "OVERDUE": {}
                    },
                    "NONSTD": {
                      "DPD 91-180": {},
                      "DPD > 180": {},
                      "SUB": {},
                      "RES": {},
                      "NPA": {},
                      "DBT": {},
                      "LOSS": {}
                    },
                    "CLOSED": {
                      "CLOSED": {}
                    },
                    "OTHERS": {
                      "OTHERS": {}
                    }
                  },
                  "AsGuarantorOnMember": {
                    "STD": {
                      "DPD 0": {},
                      "DPD 1-30": {},
                      "DPD 31-60": {},
                      "DPD 61-90": {},
                      "SMA 0": {},
                      "SMA 1": {},
                      "SMA 2": {},
                      "OVERDUE": {}
                    },
                    "NONSTD": {
                      "DPD 91-180": {},
                      "DPD > 180": {},
                      "SUB": {},
                      "RES": {},
                      "NPA": {},
                      "DBT": {},
                      "LOSS": {}
                    },
                    "CLOSED": {
                      "CLOSED": {}
                    },
                    "OTHERS": {
                      "OTHERS": {}
                    }
                  },
                  "AsGuarantorOffMember": {
                    "STD": {
                      "DPD 0": {},
                      "DPD 1-30": {},
                      "DPD 31-60": {},
                      "DPD 61-90": {},
                      "SMA 0": {},
                      "SMA 1": {},
                      "SMA 2": {},
                      "OVERDUE": {}
                    },
                    "NONSTD": {
                      "DPD 91-180": {},
                      "DPD > 180": {},
                      "SUB": {},
                      "RES": {},
                      "NPA": {},
                      "DBT": {},
                      "LOSS": {}
                    },
                    "CLOSED": {
                      "CLOSED": {}
                    },
                    "OTHERS": {
                      "OTHERS": {}
                    }
                  }
                }
              },
              "CreditFacilityDetails": [
                {
                  "account_number": "00000037005530994",
                  "sanctiondate_loanactivation": "2018-05-02",
                  "sanctioned_amount_notional_amountofcontract": "200000",
                  "currency_code": "INR",
                  "credit_type": "Medium term loan (period above 1 year and up to 3 years)",
                  "tenure_weighted_avg_maturityperiod": "60",
                  "repayment_frequency": "Monthly",
                  "drawing_power": "184719",
                  "current_balance_limit_utilized_marktomarket": "32443",
                  "loan_expiry_maturity_date": "2023-05-02",
                  "assetclassification_dayspastdue": "0 dpd",
                  "amount_overdue_limit_overdue": "0",
                  "installment_amount": "1392",
                  "account_status": "Open",
                  "asset_based_security_coverage": "Full",
                  "guarantee_coverage": "Nil",
                  "wilful_default_status": "Not Wilful Defaulter",
                  "dispute_id_no": "22",
                  "dt_reported_lst": "2020-03-31",
                  "credit_type_group": "TL",
                  "member_type": "Off-Member",
                  "sector_type": "PSU Bank-1",
                  "member_branch_cd": "11986",
                  "accountSeqNo": "1B",
                  "History48Months": [
                    {
                      "account_number": "00000037005530994",
                      "current_balance_limit_utilized_marktomarket": "32443",
                      "assetclassification_dayspastdue": "0 dpd",
                      "amount_overdue_limit_overdue": "0",
                      "account_status": "OPN",
                      "wilful_default_status": "Not Wilful Defaulter",
                      "dt_reported_lst": "2020-03-31",
                      "yyyymm": "2020-03",
                      "sanctiondate_loanactivation": "2018-05-02",
                      "sanctioned_amount_notional_amountofcontract": "200000",
                      "currency_code": "INR",
                      "credit_type": "Medium term loan (period above 1 year and up to 3 years)",
                      "tenure_weighted_avg_maturityperiod": "60",
                      "repayment_frequency": "Monthly",
                      "drawing_power": "184719",
                      "loan_expiry_maturity_date": "2023-05-02",
                      "installment_amount": "1392",
                      "asset_based_security_coverage": "Full",
                      "guarantee_coverage": "Nil",
                      "overduebucket": "DPD 0"
                    }
                  ],
                  "SecuritySgmnt": [
                    {
                      "value_of_security": "400000",
                      "currency_type": "INR",
                      "type_of_security": "Other Assets",
                      "security_classification": "Primary – First Charge",
                      "date_of_valuation": "2018-05-02"
                    }
                  ],
                  "account_status_code": "01"
                }
              ],
              "EnquirySummary": {
                "Purpose": "ALL",
                "Total": "16",
                "Past30Days": "16",
                "Past12Months": "16",
                "Past24Months": "16"
              },
              "RecentEnquiries": [
                {
                  "seq": "0",
                  "Institution": "TEST BANK",
                  "Date": "2023-12-06",
                  "Time": "07:10",
                  "Amount": "100"
                },
                {
                  "seq": "1",
                  "Institution": "TEST BANK",
                  "Date": "2024-03-04",
                  "Time": "07:14",
                  "Amount": "100"
                },
                {
                  "seq": "2",
                  "Institution": "TEST BANK",
                  "Date": "2024-05-08",
                  "Time": "09:37",
                  "Amount": "100"
                },
                {
                  "seq": "3",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-17",
                  "Time": "07:28",
                  "Amount": "100"
                },
                {
                  "seq": "4",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-08-05",
                  "Time": "05:59",
                  "Amount": "100"
                },
                {
                  "seq": "5",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-15",
                  "Time": "13:28",
                  "Amount": "100"
                },
                {
                  "seq": "6",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-24",
                  "Time": "08:13",
                  "Amount": "100"
                },
                {
                  "seq": "7",
                  "Institution": "TEST BANK",
                  "Date": "2023-11-08",
                  "Time": "09:51",
                  "Amount": "100"
                },
                {
                  "seq": "8",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-19",
                  "Time": "10:36",
                  "Amount": "100"
                },
                {
                  "seq": "9",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-17",
                  "Time": "07:17",
                  "Amount": "100"
                },
                {
                  "seq": "10",
                  "Institution": "TEST BANK",
                  "Date": "2024-05-08",
                  "Time": "09:38",
                  "Amount": "100"
                },
                {
                  "seq": "11",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-08-07",
                  "Time": "04:26",
                  "Amount": "100"
                },
                {
                  "seq": "12",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-17",
                  "Time": "07:18",
                  "Amount": "100"
                },
                {
                  "seq": "13",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-24",
                  "Time": "08:49",
                  "Amount": "100"
                },
                {
                  "seq": "14",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-07-16",
                  "Time": "04:20",
                  "Amount": "100"
                },
                {
                  "seq": "15",
                  "Institution": "HDFC Bank Limited",
                  "Date": "2024-08-05",
                  "Time": "06:02",
                  "Amount": "100"
                }
              ],
              "GurantorCFSummary": {}
            }
          }
        }
      },
      "credit_score": ""
    }
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Tue, 25 Mar 2025 09:53:05 GMT

Content-Type

application/json

Content-Length

9439

Connection

keep-alive

### POSTCredit Report Commercial PDF

https://kyc-api.surepass.io/api/v1/credit-report-commercial/fetch-report-pdf

The Credit Score API provides business commercial credit report PDF.

**Request Body**

**Key**

**Format**

**Description**

business\_name

String

Enter Business Name

pan

String

Enter PAN Number

mobile

String

Enter Mobile Number

consent

String

User Consent

raw

Boolean

JSON report included or not

`consent` can have the following values:

-   `Y`

**Response Body**

**Key**

**Format**

**Description**

client\_id

String

Unique Cllient ID

pan

String

PAN Number

mobile

String

Mobile Number

business\_name

String

Business Name

credit\_score

String

Credit Score

credit\_report

Object

Credit Report(as received from the bureau)

credit\_report\_link

String

Credit Report PDF Link

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "business_name": "SHAIK SADIQ ALI",
    "mobile": "8977715735",
    "pan": "IQGPS3724B",
    "consent": "Y"
}
```

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/credit-report-commercial/fetch-report-pdf' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "business_name": "SHAIK SADIQ ALI",
    "mobile": "8977715735",
    "pan": "IQGPS3724B",
    "consent": "Y"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "credit_report_commercial_pdf_ddwabvOTsrFGfrfYWrkj",
    "pan": "IQGPS3724B",
    "mobile": "8977715735",
    "business_name": "SHAIK SADIQ ALI",
    "credit_score": "",
    "credit_report": {},
    "credit_report_link": "https://aadhaar-kyc-docs.s3.amazonaws.com/username_2kecgbknrxrabfmh7yi2obkba3p/credit_report_commercial/credit_report_commercial_pdf_ddwabvOTsrFGfrfYWrkj/commercial_report_1742898017877581.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAY5K3QRM5FYWPQJEB%2F20250325%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20250325T102018Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=ae16178e45ba8725311894efdca31475273a0d367cfcc260c2ee4f99c730ee4a"
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Tue, 25 Mar 2025 10:20:18 GMT

Content-Type

application/json

Content-Length

770

Connection

keep-alive

## 

Customer Data Pull

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### POSTPrefill Report

https://kyc-api.surepass.io/api/v1/prefill/prefill-report-v2

This API is used to fetch customer data using their name and mobile as input.

**Request Body**

**Key**

**Format**

**Description**

name

String

Enter Name As An Input

mobile

String

Enter Mobile Number As An Input

**Response Body**

**Key**

**Format**

**Description**

client\_id

String

Unique Client ID

name

String

Full Name

mobile

String

Mobile Number

personal\_info

Object

Personal Information

phone\_info

Object

Phone Detail

address\_info

Object

Address Detail

email\_info

Object

Email Detail

identity\_info

Object

Identity Information

**personal\_info (Object)**

Key

Format

Description

full\_name

String

Full name of the person

dob

String

Date of birth in YYYY-MM-DD format

gender

String

Gender of the person (Male/Female)

total\_income

String

Total income of the person

occupation

String

Occupation of the person

age

String

Age of the person

**phone\_info (Object)**

Key

Format

Description

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

type\_code

String

Type code representing the nature of the data

number

String

Mobile Number

**address\_info (Object)**

Key

Format

Description

address

String

Full address of the person

state

String

State where the address is located

type

String

Type of address (e.g., Permanent, Temporary)

postal

String

Postal code or ZIP code

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

**email\_info (Object)**

Format

Description

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

email\_address

String

Email address associated with the reported date

**identity\_info (Object)**

Key

Format

Description

pan\_number

Object

PAN number details

passport\_number

Object

Passport number details

driving\_license

Object

Driving license details

voter\_id

Object

Voter ID details

aadhaar\_number

Object

Aadhaar number details

ration\_card

Object

Ration card details

other\_id

Object

Array of objects for other ID details

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "name": "Rajendra Singh",
    "mobile": "9660123456"
}
```

Example Request

Success

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/prefill/prefill-report-v2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "name": "Rajendra Singh",
    "mobile": "9660123456"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "prefill_report_v2_FpyRXBhdoauvQNwrQzke",
    "name": "RAJENDRA SINGH",
    "mobile": "9660123456",
    "personal_info": {
      "full_name": "RAJENDRA SINGH ",
      "dob": "1968-10-20",
      "gender": "Male",
      "total_income": "",
      "occupation": "",
      "age": "55"
    },
    "phone_info": [
      {
        "reported_date": "2024-01-28",
        "type_code": "H",
        "number": "00001427"
      },
      {
        "reported_date": "2019-07-31",
        "type_code": "M",
        "number": "9660123456"
      },
      {
        "reported_date": "2023-01-31",
        "type_code": "M",
        "number": "9660123456"
      }
    ],
    "address_info": [
      {
        "address": "S/O SHIV PRASAD SINGH MAHWA",
        "state": "RAJASTHAN",
        "type": "Permanent",
        "postal": "123456",
        "reported_date": "2024-01-28"
      },
      {
        "address": "UNIT-A-123456 RAM NAGARIA RAM NAGARIA  NEAR JAGATPURA JAIPUR JAIPUR JAIPUR",
        "state": "RAJASTHAN",
        "type": "",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "TODABHIM DIST  KARAULI PATOLI TODABHIM",
        "state": "RAJASTHAN",
        "type": "Office",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "WARD NO 4  DAUSA-123456",
        "state": "RAJASTHAN",
        "type": "Primary",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "A 1001 RAM NAGARIYA",
        "state": "RAJASTHAN",
        "type": "Owns,Permanent",
        "postal": "302017",
        "reported_date": "2019-07-31"
      }
    ],
    "email_info": [
      {
        "reported_date": "2021-06-30",
        "email_address": "VISHALRATHORE@GMAIL.COM"
      }
    ],
    "identity_info": {
      "pan_number": [
        {
          "id_number": "CMGPA1234J"
        }
      ],
      "passport_number": [],
      "driving_license": [],
      "voter_id": [
        {
          "id_number": "RJ100873123456"
        }
      ],
      "aadhaar_number": [
        {
          "id_number": "XXXXXXXXXXXX"
        }
      ],
      "ration_card": [],
      "other_id": []
    }
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Fri, 22 Mar 2024 12:32:05 GMT

Content-Type

application/json

Content-Length

1740

Connection

keep-alive

### POSTPrefill By Mobile

https://kyc-api.surepass.io/api/v1/prefill/prefill-by-mobile

This API fetches customer data using mobile as input.

**Request Body**

**Key**

**Format**

**Description**

mobile

String

Enter Mobile Number As An Input

**Response Body**

**Key**

**Format**

**Description**

client\_id

String

Unique Client ID

name

String

Full Name

mobile

String

Mobile Number

personal\_info

Object

Personal Information

phone\_info

Object

Phone Detail

address\_info

Object

Address Detail

email\_info

Object

Email Detail

identity\_info

Object

Identity Information

**personal\_info (Object)**

Key

Format

Description

full\_name

String

Full name of the person

dob

String

Date of birth in YYYY-MM-DD format

gender

String

Gender of the person (Male/Female)

total\_income

String

Total income of the person

occupation

String

Occupation of the person

age

String

Age of the person

**phone\_info (Object)**

Key

Format

Description

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

type\_code

String

Type code representing the nature of the data

number

String

Mobile Number

**address\_info (Object)**

Key

Format

Description

address

String

Full address of the person

state

String

State where the address is located

type

String

Type of address (e.g., Permanent, Temporary)

postal

String

Postal code or ZIP code

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

**email\_info (Object)**

Format

Description

reported\_date

String

Date when the information was reported in YYYY-MM-DD format

email\_address

String

Email address associated with the reported date

**identity\_info (Object)**

Key

Format

Description

pan\_number

Object

PAN number details

passport\_number

Object

Passport number details

driving\_license

Object

Driving license details

voter\_id

Object

Voter ID details

aadhaar\_number

Object

Aadhaar number details

ration\_card

Object

Ration card details

other\_id

Object

Array of objects for other ID details

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "mobile": "9660912345"
}
```

Example Request

Success

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/prefill/prefill-by-mobile' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "mobile": "9660912345"
}'
```

Example Response

-   Body
-   Headers (1)

View More

json

```json
{
  "data": {
    "client_id": "prefill_report_v2_FpyRXBhdoauvQNwrQzke",
    "name": "RAJENDRA SINGH",
    "mobile": "9660123456",
    "personal_info": {
      "full_name": "RAJENDRA SINGH ",
      "dob": "1968-10-20",
      "gender": "Male",
      "total_income": "",
      "occupation": "",
      "age": "55"
    },
    "phone_info": [
      {
        "reported_date": "2024-01-28",
        "type_code": "H",
        "number": "00001427"
      },
      {
        "reported_date": "2019-07-31",
        "type_code": "M",
        "number": "9660123456"
      },
      {
        "reported_date": "2023-01-31",
        "type_code": "M",
        "number": "9660123456"
      }
    ],
    "address_info": [
      {
        "address": "S/O SHIV PRASAD SINGH MAHWA",
        "state": "RAJASTHAN",
        "type": "Permanent",
        "postal": "123456",
        "reported_date": "2024-01-28"
      },
      {
        "address": "UNIT-A-123456 RAM NAGARIA RAM NAGARIA  NEAR JAGATPURA JAIPUR JAIPUR JAIPUR",
        "state": "RAJASTHAN",
        "type": "",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "TODABHIM DIST  KARAULI PATOLI TODABHIM",
        "state": "RAJASTHAN",
        "type": "Office",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "WARD NO 4  DAUSA-123456",
        "state": "RAJASTHAN",
        "type": "Primary",
        "postal": "123456",
        "reported_date": "2023-01-31"
      },
      {
        "address": "A 1001 RAM NAGARIYA",
        "state": "RAJASTHAN",
        "type": "Owns,Permanent",
        "postal": "302017",
        "reported_date": "2019-07-31"
      }
    ],
    "email_info": [
      {
        "reported_date": "2021-06-30",
        "email_address": "VISHALRATHORE@GMAIL.COM"
      }
    ],
    "identity_info": {
      "pan_number": [
        {
          "id_number": "CMGPA1234J"
        }
      ],
      "passport_number": [],
      "driving_license": [],
      "voter_id": [
        {
          "id_number": "RJ100873123456"
        }
      ],
      "aadhaar_number": [
        {
          "id_number": "XXXXXXXXXXXX"
        }
      ],
      "ration_card": [],
      "other_id": []
    }
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Content-Type

application/json

## 

MCA Docs Download

# MCA API

### MCA Response Object

Key

Format

Description

client\_id

String

Unique Client ID

entity\_type

String

"company" or "llp"

entity\_name

String

Name of the company

status

String

"pending" or "failed" or "paused" or "partially\_completed" or "completed"

mca\_payment

Boolean

Whether payment was made for this particular order

mca\_srn

String

MCA SRN number

fetch\_only

Boolean

Fetch only mode or not

fetched

Boolean

Documents list fetched or not. Applicable only in "fetch only" mode

documents

Array of Objects

[Documents Object](#documents-object)

### Documents Object

Key

Format

Description

document\_id

String

Unique ID for this document

document\_name

String

Name of the document

category

String

Category of the document

status

String

"pending" or "completed" or "failed"

document\_url

String

URL to download the document

### Create Order

Create an MCA order.

#### Request Body

Key

Format

Description

entity\_id\*

String

CIN or LLPIN of the company the documents are required

mca\_username

String

Username of MCA account

mca\_password

String

Password of MCA account

fetch\_only

Boolean

Lazy download of MCA docs. Default `false`

webhook\_url

String(URL)

Webhook URL

> (\*) Required Field

Notes:

-   By default we use our own MCA account to download documents. You can provide `mca_username` and `mca_password` if you want us to use your account.
-   For testing in sandbox envrionment only the following `entity_id` are valid
    
    -   `U72900MH2007PTC179997`: For status "pending"
    -   `U72900MH2007PTC179998`: For status "failed"
    -   `U72900MH2007PTC179999`: For status "completed"
    
-   Webhook secret must be set via API before using `webhook_url`.

### Lazy fetching of Documents

If you want pre-fetch the list of MCA documents, and lazily download only a select set of documents you can use the "**fetch only**" mode, by setting the `fetch_only` param to `true` in the API request.

In this mode we will create an order in `paused` state and fetch list of available documents from MCA. Then using the [Register feteched order API](#register-fetched-order) you can provide the list of document IDs which you want to download.

### Register Fetched Order

Download selected documents from order in `paused` state.

#### Request Body

Key

Format

Description

client\_id

String

Unique Client ID

documents

Array of String

List of `document_id` to download

### Get Status

To get the staus of MCA order.

#### Response Body

[MCA Response Object](#mca-response-object)

Notes:

-   `status` can be one of "pending", "paused", "partial", "failed" or "completed", denoting the status if the order.
-   `mca_payment` indicates the status whether the payment was made to MCA or not.

### MCA Webhook

If you want to receieve webhook after the list of documents if fetched or the order is completed, you can pass a `webhook_url` in the request body. Make sure you have the webhook secret to validate the incoming webhook.

There are two types of MCA webhook events, `MCA_FETCH_DOCS` and `MCA_ORDER`. `MCA_FETCH_DOCS` is sent when we have fetched the list of available documents in "fetch only" mode. `MCA_ORDER` is sent when the order is completed, that is, we have downloaded the documents.

#### Webhook Object

Key

Format

Description

event

String Enum

Type of event. One of `MCA_ORDER` or `MCA_FETCH_DOCS`

data

Object

[MCA Response Object](#mca-response-object)

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

## 

Ecourts

APIs related to Ecourts in India.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

## 

Ecourts Search

This API is used to retrieve information about a legal case involving an individual. It provides various details about the case, including the names of involved parties, addresses, case specifics, and court information.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### POSTEcourts Search V2

https://kyc-api.surepass.io/api/v1/ecourts/ecourt-search-v2

**Request Body**

**Key**

**Format**

**Description**

name

String

Name of the accused

father\_name

String

Accused Father Name

address

String

Accused Full Address

year

String

Case Year

state

String

State Name

**Response Body**

Key

Format

Description

client\_id

String

Unique Client ID

name

String

Accused Name

father\_name

String

Accused Father Name

address

String

Accused Full Address

year

String

Case Year

state

String

State Name

result

Object

Full Details of accused

**result (Object)**

View More

Key

Format

Description

year

String

Year of the case

bench

String

Bench where the case was heard

crawling\_date

String

Date when the case data was crawled

judgement\_date

String

Date of the judgement

judgement\_description

String

Description of the judgement

case\_flow

Object

Flow of case orders and their details

order\_flow

Object

Flow of court orders

petitioner

String

Name of the petitioner

state\_code

String

Code of the state

dist\_code

String

Code of the district

court\_number

String

Court number

registration\_number

String

Registration number of the case

filing\_number

String

Filing number of the case

filing\_date

String

Date when the case was filed

hearing\_date

string

Date when the hearing was held

court\_number\_and\_judge

String

Court number and judge details

respondent

String

Name of the respondent

case\_name

String

Name of the case

case\_type\_name

String

Type of the case

case\_type\_number

String

Number associated with the case type

court\_name

String

Name of the court

case\_status

String

Status of the case

case\_no

String

Case number

fir\_number

String

FIR number associated with the case

fir\_link

String

Link to the FIR

dist

String

District

police\_station

String

Police station associated with the case

circle

String

Circle

state

String

State where the case was filed

court\_type

String

Type of the court

district

String

District where the case was heard

case\_link

String

Link to the case details

suit\_filed\_amount

String

Amount for which the suit was filed

gfc\_updated\_at

String

Date when the case details were last updated

created\_at

String

Date when the case record was created

cnr\_number

String

CNR number of the case

case\_reg\_date

String

Registration date of the case

petitioner\_address

String

Address of the petitioner

respondent\_address

String

Address of the respondent

under\_act

String

Act under which the case was filed

under\_section

String

Section under which the case was filed

nature\_of\_disposal

String

Nature of the case disposal

gfc\_respondents

Object

List of respondents with their details

gfc\_petitioners

Object

List of petitioners with their details

gfc\_fir\_respondents

Object

List of FIR respondents with their details

gfc\_fir\_petitioners

Object

List of FIR petitioners with their details

case\_details\_link

String

Link to the case details

gfc\_fir\_number\_court

String

FIR number in the court records

gfc\_fir\_year\_court

String

Year of the FIR in the court records

gfc\_fir\_policestation\_court

String

Police station associated with the FIR in the court records

gfc\_orders\_data

object

Data related to the orders in the case

**case\_flow (Object)**

Key

Format

Description

order

String

Order description

gfc\_order\_type

String

Type of the order

order\_date

String

Date of the order

order\_link

String

Order PDF link

**gfc\_respondents (Object)**

Key

Format

Description

name

String

Name of the respondent

**gfc\_petitioners (Object)**

Key

Format

Description

name

String

Name of the petitioner

**gfc\_orders\_data (Object)**

**Key**

**Format**

**Description**

petitioners

Object

Petitioners Comprehensive details

respondents

Object

Respodentes Comprehensive details

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "name": "Gagan Sharma",
    "father_name": "Ramesh Chand Sharma",
    "address": "ramnagariya jagatpura jaipur",
    "year": "2020",
    "state": ""
}
```

Example Request

Success

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/ecourts/ecourt-search-v2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "name": "Gagan Sharma",
    "father_name": "Ramesh Chand Sharma",
    "address": "ramnagariya jagatpura jaipur",
    "year": "2020",
    "state": ""
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```
{
  "data": {
    "client_id": "ecourt_search_v2_mxyvrmamIseuShYppgru",
    "name": "MEGHNA SAUMYA GANDHI",
    "father_name": "HARSHAD PRANLAL KOTHARI",
    "address": "1902/ RUSTOMJEE ADARSH EXCELLENCY C.H.S$OFF MARVE ROAD, NEAR CARMEL SCHOOL MALAD WEST MUMBAI MH  400064",
    "year": "2016",
    "state": "Maharashtra",
    "result": [
      {
        "year": "2012",
        "bench": "",
        "crawling_date": "2022-03-29T03:25:16.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [
          {
            "order": "Order",
            "gfc_order_type": "Order",
            "order_date": "2019-12-24",
            "order_link": "https://ecourt-cdn.surepass.io?424dfa207b97727274e521181a1667b68da7776a1f28ad984794f75ef0ae507bd4dbe48c9cd17316ed9cc41edb5d417f12dd5e64672d557aa1da22a2b2e282a4"
          }
        ],
        "order_flow": [],
        "petitioner": "MS. AMARDEEP TRADING COMPANY PRO-MR. HITESH LAKHAM",
        "state_code": "1",
        "dist_code": "23",
        "court_number": "1",
        "registration_number": "2800665/2012",
        "filing_number": "100665/2012",
        "filing_date": "19-04-2012",
        "hearing_date": "18th June 2012",
        "court_number_and_judge": "6-M.M. , 28TH COURT",
        "respondent": "1. MRS. MEGHNA KRUNAL SANGHVI AND ANR",
        "case_name": "Ss casess  SS/2800665/2012",
        "case_type_name": "Ss casess  SS",
        "case_type_number": "3",
        "court_name": "Chief Metropolitan Magistrate, Esplanade Court, Mumbai",
        "case_status": "Pending",
        "case_no": "200328006652012",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Maharashtra",
        "court_type": "District Court",
        "district": "Mumbai Cmm Courts",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "10th May 2023",
        "created_at": "26th September 2023",
        "cnr_number": "MHMM110017162012",
        "case_reg_date": "19-04-2012",
        "petitioner_address": "1) MS. AMARDEEP TRADING COMPANY PRO-MR. HITESH LAKHAM    Address  - 191, DADI SHETH AGIARY LANE, MUM-2    Advocate- GAURAV G. DAVE",
        "respondent_address": "1) 1. MRS. MEGHNA KRUNAL SANGHVI AND ANR    Address - NEW VAISHALI CO-OP, HOUSING SOC LTD FLAT NO.503, NARSHINGH LANE,OPP N.M. COLLEGE, MALAD W MUM2)  2.MR. KRUNAL SANGHAVI    NEW VAISHALI CO-OP. HOUSING SOCIETY LTD FLAT NO.50",
        "under_act": "N. I. Act",
        "under_section": "138R-W141AND142",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "1. MRS. MEGHNA KRUNAL SANGHVI AND ANR",
            "address": "NEW VAISHALI CO-OP, HOUSING SOC LTD FLAT NO.503, NARSHINGH LANE,OPP N.M. COLLEGE, MALAD W MUM"
          },
          {
            "name": "2.MR. KRUNAL SANGHAVI",
            "address": "NEW VAISHALI CO-OP. HOUSING SOCIETY LTD FLAT NO.50"
          }
        ],
        "gfc_petitioners": [
          {
            "name": "MS. AMARDEEP TRADING COMPANY PRO-MR. HITESH LAKHAM",
            "address": "191, DADI SHETH AGIARY LANE, MUM-2"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=79a797df81de2d5c0d5eda509b2fdbe5709a4af9c89d4a31300642f062b9bece97a8bd1ceb042e267ce4763abe1a2dcb9b3aa87248fd61f1d48698a9625b82ad",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Criminal"
      },
      {
        "year": "2014",
        "bench": "",
        "crawling_date": "2022-03-19T03:26:51.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [
          {
            "order": "Copy of Judgment",
            "gfc_order_type": "Judgement",
            "order_date": "23-08-2016",
            "order_link": "https://ecourt-cdn.surepass.io?3a50783db741b3bea7ca81dcdfe29b2a37a4f14aa0c8ad2b35916216319e33a04a6e0520c9ccccdbddd0be60df260cfb3b5714c271707113bed414ec7d29aa63"
          },
          {
            "order": "Copy of Judgment",
            "gfc_order_type": "Judgement",
            "order_date": "23-08-2016",
            "order_link": ""
          }
        ],
        "order_flow": [],
        "petitioner": "",
        "state_code": "1",
        "dist_code": "42",
        "court_number": "11",
        "registration_number": "",
        "filing_number": "",
        "filing_date": "",
        "hearing_date": "",
        "court_number_and_judge": "",
        "respondent": "",
        "case_name": "Petition A/103089/2014",
        "case_type_name": "Petition A",
        "case_type_number": "1",
        "court_name": "Family Court, Bandra, Mumbai",
        "case_status": "Disposed",
        "case_no": "200101030892014",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Maharashtra",
        "court_type": "District Court",
        "district": "Maharashtra-Family Courts",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "25th July 2023",
        "created_at": "2nd October 2023",
        "cnr_number": "MHFC010075402014",
        "case_reg_date": "",
        "petitioner_address": "1) XXXXXXX    Address  - XXXXXXX",
        "respondent_address": "1) XXXXXXX    Address - XXXXXXX2)  XXXXXXX    XXXXXXX",
        "under_act": "HINDU MARRIAGE ACT",
        "under_section": "13(1)(ia)(ib)",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "XXXXXXX",
            "address": "XXXXXXX"
          },
          {
            "name": "XXXXXXX",
            "address": "XXXXXXX"
          }
        ],
        "gfc_petitioners": [
          {
            "name": "XXXXXXX",
            "address": "XXXXXXX"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=e06c479de8c656064da515fcee4d5b2eed906fdf08b2bd9dd34ba3a2211a3ee4ed7e01fcc32cf5016f1e312e428436075a58f774c573780d6267a384e67d0e89",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [
            {
              "pincode": "400064",
              "localityname": "mumbai malad west dely",
              "address": "residing at 10011002, Sevilla, Raheja Exotica, Patilwadi, Madh Island, Malad West Mumbai 400 064 Petitioner",
              "subdistname": "MUMBAI",
              "statename": "MAHARASHTRA",
              "lastname": "",
              "districtname": "MUMBAI",
              "name": "Mrs Meghna Rajkumar nee Meghna Bharat,",
              "id": "1",
              "age": "26"
            }
          ],
          "respondents": [
            {
              "pincode": "413507",
              "localityname": "andora kallam",
              "address": "resident of 101, Sai Gokul, Central Excise Colony,Bagh, Amberpeth, Hyderabad 500 013, Andhra Pradesh Respondent",
              "subdistname": "KALAMB",
              "statename": "MAHARASHTRA",
              "lastname": "",
              "districtname": "OSMANABAD",
              "name": "Mr Rajkumar Madhavan So Srinivas Madhavan,",
              "id": "1",
              "age": "31"
            }
          ]
        },
        "case_type": "Civil"
      },
      {
        "year": "2012",
        "bench": "",
        "crawling_date": "2022-03-29T03:11:09.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [
          {
            "order": "Order Number 1",
            "gfc_order_type": "Order",
            "order_date": "21-08-2012",
            "order_link": "https://ecourt-cdn.surepass.io?5639db02389e85d0c3832bd54841b910a3a8b0464fbf660032d8634767dcb02fd38eadb6c2be3bb44445226e81cd10461d24a84927d7f7f494aac5d503ce8623"
          }
        ],
        "order_flow": [],
        "petitioner": "Dhaku P. Ghadigaonkar",
        "state_code": "1",
        "dist_code": "37",
        "court_number": "3",
        "registration_number": "201240/2012",
        "filing_number": "201240/2012",
        "filing_date": "11-05-2012",
        "hearing_date": "15th June 2012",
        "court_number_and_judge": "2-Judge  Additional Sessions Judge",
        "respondent": "Meghana M. Ghadigonkar",
        "case_name": "Notice of Motion/201240/2012",
        "case_type_name": "Notice of Motion",
        "case_type_number": "85",
        "court_name": "Civil Court, Dindoshi",
        "case_status": "Disposed",
        "case_no": "208502012402012",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Maharashtra",
        "court_type": "District Court",
        "district": "Mumbai City Civil Court",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "10th May 2023",
        "created_at": "26th September 2023",
        "cnr_number": "MHCC040011402012",
        "case_reg_date": "11-05-2012",
        "petitioner_address": "1) Dhaku P. Ghadigaonkar    Address  - Address- R.No.2,Parag Chawl,Baman Wada Hill,Justic M.C.Chhagala Marg,Vile Parle E,Mum99.    Advocate- M.K. Ghadigaonkar",
        "respondent_address": "1) Meghana M. Ghadigonkar    Address - Jai Ganesh CHS Ltd.Kanu Compound,Santosh Nagar,Malad E,Mum97.",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": "Contested--Allowed",
        "gfc_respondents": [
          {
            "name": "Meghana M. Ghadigonkar",
            "address": "Jai Ganesh CHS Ltd.Kanu Compound,Santosh Nagar,Malad E,Mum97."
          }
        ],
        "gfc_petitioners": [
          {
            "name": "Dhaku P. Ghadigaonkar",
            "address": "Address- R.No.2,Parag Chawl,Baman Wada Hill,Justic M.C.Chhagala Marg,Vile Parle E,Mum99."
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=60d4050bf58a5443069a0de22bae79a6bcef02b309a9c9bd95a0f8aeb8a20aedf5435aef27a7cc885fe9d1353f3fba6d26984d74e6e5510a97583310056f3d97",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [
            {
              "pincode": "",
              "localityname": "",
              "address": "",
              "subdistname": "",
              "statename": "",
              "lastname": "",
              "districtname": "",
              "name": "BORIVALI DIVISION, (BRANCH)",
              "id": 1,
              "age": ""
            },
            {
              "pincode": "",
              "localityname": "",
              "address": "",
              "subdistname": "",
              "statename": "",
              "lastname": "ghadigaonkar",
              "districtname": "",
              "name": "Mr.Dhaku Rajaram Ghadigaonkar",
              "id": 2,
              "age": ""
            }
          ],
          "respondents": [
            {
              "pincode": "",
              "localityname": "",
              "address": "",
              "subdistname": "",
              "statename": "",
              "lastname": "",
              "districtname": "",
              "name": "Mrs.Meghana Manohar Ghadigaonkar & Ors.",
              "id": 1,
              "age": ""
            }
          ]
        },
        "case_type": "Civil"
      },
      {
        "year": "2008",
        "bench": "",
        "crawling_date": "2018-03-05T02:21:26.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [],
        "order_flow": [],
        "petitioner": "SMTI MEGHNA AGARWAL @ SAUMYA AGARWAL",
        "state_code": "6",
        "dist_code": "0",
        "court_number": "",
        "registration_number": "5/2008",
        "filing_number": "5/2008",
        "filing_date": "14-03-2008",
        "hearing_date": "14th March 2008",
        "court_number_and_judge": "",
        "respondent": "SRI PRAVEEN AGARWAL",
        "case_name": "Tr.P.(C)./5/2008",
        "case_type_name": "Tr.P.(C). - Transfer Petition under Section 24 C.P.C.",
        "case_type_number": "204",
        "court_name": "High Court of Gauhati",
        "case_status": "Disposed",
        "case_no": "220400000052008",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Assam",
        "court_type": "High Court",
        "district": "",
        "case_link": "https://hcservices.ecourts.gov.in",
        "suit_filed_amount": "",
        "gfc_updated_at": "25th May 2023",
        "created_at": "19th May 2023",
        "cnr_number": "GAHC010013042008",
        "case_reg_date": "14-03-2008",
        "petitioner_address": "1) SMTI MEGHNA AGARWAL @ SAUMYA AGARWAL    Address  - W/O SRI PRAVEEN AGARWAL AT PRESENT RESIDING AT   C/O SRI MAHABIR PRASAD BUKALSARIA, NEAR JAIN MANDIR, NEW MARKET, DIBRUGARH,   DIST. DIBRUGARH, ASSAM.    Advocate- MR.A KABRA,, MS.A BARUA,MR.R L YADAV,MS.K YADAV",
        "respondent_address": "1) SRI PRAVEEN AGARWAL    Address - S/O SRI JUGAL KISHORE AGARWAL,  BY CASTE HINDU, BY PROFESSION BUSINESSMAN, RESIDENT OF HAIBARGAON, OID A.T. ROAD, MOUZA NAGAON TOWN, DIST. NAGAON, ASSAM,  AND ALSO AT-B-405, PUBALI APARTMENT, BARTHAKUR MILL ROAD, ULUBARI, GHY, DIST. KAMRUP, ASSAM.Advocate- , ",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": " --",
        "gfc_respondents": [
          {
            "name": "SRI PRAVEEN AGARWAL ",
            "address": " "
          }
        ],
        "gfc_petitioners": [
          {
            "name": "SMTI MEGHNA AGARWAL @ SAUMYA AGARWAL ",
            "address": "address  -   wifeof sri praveen agarwal at present residing at   c/o sri mahabir prasad bukalsaria, near jain mandir, new market, dibrugarh,   dist. dibrugarh, assam. "
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=8041a012f319b53e439dbd2845b02202a7c88a953f5c99d66fa3a79f9abbb6022fd415ce90442f8c066e6fcfa92d581d7c155ccab2d46b8e7f827ecd7b5b0985e612baf492f3de38fad18b87e53ecf49e897679e27270c7daf7f1def652dc650",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Civil"
      },
      {
        "year": "2008",
        "bench": "",
        "crawling_date": "2017-10-02T05:32:38.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [],
        "order_flow": [],
        "petitioner": "SMTI MEGHNA AGARWAL @ SAUMYA AGARWALW/O SRI PRAVEEN AGARWAL AT PRESENT RESIDING AT \r\nC/O SRI MAHABIR PRASAD BUKALSARIA, NEAR JAIN MANDIR, NEW MARKET, DIBRUGARH, \r\nDIST. DIBRUGARH, ASSAM.",
        "state_code": "6",
        "dist_code": "0",
        "court_number": "0",
        "registration_number": "",
        "filing_number": "",
        "filing_date": "",
        "hearing_date": "",
        "court_number_and_judge": "",
        "respondent": "SRI PRAVEEN AGARWALS/O SRI JUGAL KISHORE AGARWAL,\r\nBY CASTE HINDU, BY PROFESSION BUSINESSMAN, RESIDENT OF HAIBARGAON, OID A.T. ROAD, MOUZA NAGAON TOWN, DIST. NAGAON, ASSAM,\r\nAND ALSO AT-B-405, PUBALI APARTMENT, BARTHAKUR MILL ROAD, ULUBARI, GHY, DIST. KAMRUP, ASSAM.Category Code  10245 ( Civil Revisions for transfer of suit under Section 24 of the CPC )District  DibrugarhCase Summary  Registration Date  14/03/2008Last Date of Listing\t  19/08/2009Last Stage of Listing  ADMISSIONLast Court No  4Last Date of Disposal  19/08/2009Last Order  Disposed Of",
        "case_name": "",
        "case_type_name": "",
        "case_type_number": "",
        "court_name": "High Court of Gauhati",
        "case_status": "Disposed",
        "case_no": "Tr.P.(C). 5/2008",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Assam",
        "court_type": "High Court",
        "district": "",
        "case_link": "https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=6&dist_cd=1&court_code=1&stateNm=Assam",
        "suit_filed_amount": "",
        "gfc_updated_at": "25th May 2023",
        "created_at": "19th May 2023",
        "cnr_number": "",
        "case_reg_date": "14/03/2008",
        "petitioner_address": "",
        "respondent_address": "",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "SRI PRAVEEN AGARWAL sonof  SRI JUGAL KISHORE AGARWAL,\r BY CASTE HINDU, BY PROFESSION BUSINESSMAN",
            "address": "HAIBARGAON, OID A.T. ROAD, MOUZA NAGAON TOWN, DIST. NAGAON, ASSAM,\r AND ALSO AT-B-405, PUBALI APARTMENT, BARTHAKUR MILL ROAD, ULUBARI, GHY, DIST. KAMRUP, ASSAM.Category Code  10245 ( Civil Revisions for transfer of suit under Section 24 of the CPC )District  DibrugarhCase Summary  Registration Date  14/03/2008Last Date of Listing\t  19/08/2009Last Stage of Listing  ADMISSIONLast Court No  4Last Date of Disposal  19/08/2009Last Order  Disposed Of"
          }
        ],
        "gfc_petitioners": [
          {
            "name": "SMTI MEGHNA AGARWAL @ SAUMYA AGARWAL wifeof  SRI PRAVEEN AGARWAL AT PRESENT",
            "address": "C/O SRI MAHABIR PRASAD BUKALSARIA, NEAR JAIN MANDIR, NEW MARKET, DIBRUGARH, \r DIST. DIBRUGARH, ASSAM"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=a22ebd86520df5c0f19bd719b4866341dfb5810a8f700268e70c36f35c75f6f3",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": ""
      },
      {
        "year": "2014",
        "bench": "",
        "crawling_date": "2022-03-19T04:20:38.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [],
        "order_flow": [],
        "petitioner": "MS M. DARUWALLA AND SON",
        "state_code": "1",
        "dist_code": "37",
        "court_number": "1",
        "registration_number": "101295/2014",
        "filing_number": "108387/2014",
        "filing_date": "25-07-2014",
        "hearing_date": "",
        "court_number_and_judge": "56-COURT 56 ADDITIONAL SESSIONS JUDGE",
        "respondent": "1.SANJAY KEDIA 2. MEGHNA SANJAY KEDIA 3. MR. PERCY KUTAR",
        "case_name": "SUMMARY CIVIL SUIT/101295/2014",
        "case_type_name": "SUMMARY CIVIL SUIT",
        "case_type_number": "59",
        "court_name": "City Civil Court, Mumbai",
        "case_status": "Pending",
        "case_no": "205901012952014",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Maharashtra",
        "court_type": "District Court",
        "district": "Mumbai City Civil Court",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "3rd May 2023",
        "created_at": "2nd October 2023",
        "cnr_number": "MHCC010078382014",
        "case_reg_date": "11-08-2014",
        "petitioner_address": "1) MS M. DARUWALLA AND SON    Address  - 530 A, ARVIND NIWAS, ROOM NO.4, SANDHURST BRIDGE, OPERA HOUSE, MUMBAI-400007    Advocate- PRASAD L. GAJBHIYE, Rajiv A Jadhav",
        "respondent_address": "1) 1.SANJAY KEDIA 2. MEGHNA SANJAY KEDIA 3. MR. PERCY KUTAR    Address - 1ST TWO ARE AT, 4401, C BELLISIOMO, MAHALAXMI, MUMBAI. 3.4.4 DESIGN, 302, VASAN UDYOG BHAVAN,LOWER PAREL, MUMBAI.",
        "under_act": "C.P.C.- Non-Interlocutory Order",
        "under_section": "9",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "1.SANJAY KEDIA 2. MEGHNA SANJAY KEDIA 3. MR. PERCY KUTAR",
            "address": "1ST TWO ARE AT, 4401, C BELLISIOMO, MAHALAXMI, MUMBAI. 3.4.4 DESIGN, 302, VASAN UDYOG BHAVAN,LOWER PAREL, MUMBAI."
          }
        ],
        "gfc_petitioners": [
          {
            "name": "MS M. DARUWALLA AND SON",
            "address": "530 A, ARVIND NIWAS, ROOM NO.4, SANDHURST BRIDGE, OPERA HOUSE, MUMBAI-400007"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=a29458af8aaff35d1e6bf38e52c4f9cf84889eb9c1abefe50cd61b87b3ddbcda8e0bf2545348f834808f5b06088c60877d9711bb595e93b439797c24160b9db6",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Civil"
      },
      {
        "year": "2018",
        "bench": "",
        "crawling_date": "2019-11-24T10:21:07.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [
          {
            "order": "COPY OF ORDER",
            "gfc_order_type": "Order",
            "order_date": "2019-05-17",
            "order_link": "https://ecourt-cdn.surepass.io?15b762c3771214ecd3a542cec97e526e380b901ce4cd598468e768347b3f6f89acfbfa19b12dcf3853fcf841b9bd5cb2fc32c88e7d5bfbb579722b2ee15c664e"
          },
          {
            "order": "COPY OF ORDER",
            "gfc_order_type": "Order",
            "order_date": "2019-01-30",
            "order_link": "https://ecourt-cdn.surepass.io?15b762c3771214ecd3a542cec97e526e380b901ce4cd598468e768347b3f6f89f0b518fbbaf03ce9951361d661ddf4a5b939045a857067d36a73c2fc16dfcf69"
          },
          {
            "order": "COPY OF ORDER",
            "gfc_order_type": "Order",
            "order_date": "2018-10-04",
            "order_link": "https://ecourt-cdn.surepass.io?9d5ee6735c0f57f4102fc001657de11e9cc7f6193a4ea5453820558159d84eb23bd53b61d964b8e0fc3a67f8c80aa9ee93f054aa41c75db950271f9ebcb3c966"
          }
        ],
        "order_flow": [],
        "petitioner": "STATE",
        "state_code": "26",
        "dist_code": "8",
        "court_number": "2",
        "registration_number": "12101/2018",
        "filing_number": "28292/2018",
        "filing_date": "10-09-2018",
        "hearing_date": " 04th October 2018",
        "court_number_and_judge": "591-Metropolitan Magistrate",
        "respondent": "GURPREET SINGH OBEROI",
        "case_name": "Cr. Case/12101/2018",
        "case_type_name": "Cr. Case",
        "case_type_number": "21",
        "court_name": "Chief Metropolitan Magistrate, Central, THC",
        "case_status": "Disposed",
        "case_no": "202100121012018",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Delhi",
        "court_type": "District Court",
        "district": "Central",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "5th January 2023",
        "created_at": "10th February 2023",
        "cnr_number": "DLCT020283712018",
        "case_reg_date": "10-09-2018",
        "petitioner_address": "1) STATE2)  MEGHNA KHATURIA    R/O C-210, HOSTEL II, IIT BOMBAY POWEI MUMBAI - 400076",
        "respondent_address": "1) GURPREET SINGH OBEROI ",
        "under_act": "IPC",
        "under_section": "380",
        "nature_of_disposal": "Uncontested--PLEAD GUILTY",
        "gfc_respondents": [
          {
            "name": "GURPREET SINGH OBEROI"
          }
        ],
        "gfc_petitioners": [
          {
            "name": "STATE"
          },
          {
            "name": "MEGHNA KHATURIA",
            "address": "r/o c-210, hostel ii, iit bombay powei mumbai - 400076"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=5aa7340634aceca830c892a7168fb3ef36ae15f9ec80590d9c9a18f3170847b574b305407616bf2598a0bc8a3555b3e206ef5d831c8de45ad696be56174dbf1e",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Criminal"
      },
      {
        "year": "2011",
        "bench": "",
        "crawling_date": "2022-04-02T00:46:11.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [],
        "order_flow": [],
        "petitioner": "JIGNESH KIRITKUMAR CAGNDHI",
        "state_code": "17",
        "dist_code": "13",
        "court_number": "21",
        "registration_number": "366/2011",
        "filing_number": "366/2011",
        "filing_date": "02-05-2011",
        "hearing_date": "22nd June 2011",
        "court_number_and_judge": "53-",
        "respondent": "MIISSIONARIES OF CHARITY",
        "case_name": "CMA DC/366/2011",
        "case_type_name": "CMA DC",
        "case_type_number": "3",
        "court_name": "CITY CIVIL AND SESSIONS COURT, AHMEDABAD",
        "case_status": "Disposed",
        "case_no": "200300003662011",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Gujarat",
        "court_type": "District Court",
        "district": "Ahmedabad",
        "case_link": "https://services.ecourts.gov.in/ecourtindia_v6/",
        "suit_filed_amount": "",
        "gfc_updated_at": "10th May 2023",
        "created_at": "4th October 2023",
        "cnr_number": "GJAH020003662011",
        "case_reg_date": "04-05-2011",
        "petitioner_address": "1) JIGNESH KIRITKUMAR CAGNDHI    Address  - B-605, SURYA PLAZA, UDHNA MAGDALA, ROAD, SURAT, ,SURAT    Advocate- K.S.RAVAL2)  MEGHNA JIGNESH GANDHI    B-605, SURYA PLAZA, UDHNA MAGDALA, ROAD, SURAT, ,SURAT    Advocate-K.S.RAVAL",
        "respondent_address": "1) MIISSIONARIES OF CHARITY    Address - OFFICE AT BHIMJIPURA NAVA WADAJ, AHMEDABAD,AHMEDABAD",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": "Contested--JUDGEMENT",
        "gfc_respondents": [
          {
            "name": "MIISSIONARIES OF CHARITY",
            "address": "OFFICE AT BHIMJIPURA NAVA WADAJ, AHMEDABAD,AHMEDABAD"
          }
        ],
        "gfc_petitioners": [
          {
            "name": "JIGNESH KIRITKUMAR CAGNDHI",
            "address": "B-605, SURYA PLAZA, UDHNA MAGDALA, ROAD, SURAT, ,SURAT"
          },
          {
            "name": "MEGHNA JIGNESH GANDHI",
            "address": "B-605, SURYA PLAZA, UDHNA MAGDALA, ROAD, SURAT, ,SURAT"
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=388dcb79ce66977f47dbfadf81c51320218c31986193ec77308c14a5ee5accec53d6fda4a18a4a5c3d5f226b54397221211000c75702caae38997c0eae1227ec",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Civil"
      },
      {
        "year": "2016",
        "bench": "",
        "crawling_date": "2017-10-04T09:28:43.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [],
        "order_flow": [],
        "petitioner": "ANAND GANDHI",
        "state_code": "2",
        "dist_code": "0",
        "court_number": "",
        "registration_number": "",
        "filing_number": "",
        "filing_date": "27-01-2016",
        "hearing_date": "",
        "court_number_and_judge": "",
        "respondent": "MRS. MEGHNA GANDHI",
        "case_name": "",
        "case_type_name": "CRP - CIVIL REVISION PETITION\r",
        "case_type_number": "",
        "court_name": "High Court of Andhra Pradesh",
        "case_status": "Pending",
        "case_no": "CRP728/2016",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Andhra Pradesh",
        "court_type": "High Court",
        "district": "",
        "case_link": "https://aphc.gov.in/csis_ap/",
        "suit_filed_amount": "",
        "gfc_updated_at": "24th June 2023",
        "created_at": "22nd June 2023",
        "cnr_number": "",
        "case_reg_date": "09-02-2016",
        "petitioner_address": "",
        "respondent_address": "",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "MRS. MEGHNA GANDHI "
          }
        ],
        "gfc_petitioners": [
          {
            "name": "ANAND GANDHI "
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=40419c6772e6a8a7b2535f71795fde4aa46b186c90bafaa64be6be1cc81e8349006133e12ebcf2466a188e8ab70e72c4820a07a17564317cebe5da589d45ce70",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": "Civil"
      },
      {
        "year": "2021",
        "bench": "",
        "crawling_date": "2021-07-31T13:56:04.000Z",
        "judgement_date": "",
        "judgement_description": "",
        "case_flow": [
          {
            "order": "Spl Cell Orders",
            "gfc_order_type": "Order",
            "order_date": "2021-11-23",
            "order_link": "https://ecourt-cdn.surepass.io?68a78ed32405fea773896c5ed5d51d2c471d3a3368c4cb7e1b6f08174fa71b2422dd65f69f633ee25d274c4c38a34bb4"
          },
          {
            "order": "Spl Cell Orders",
            "gfc_order_type": "Order",
            "order_date": "2021-11-19",
            "order_link": "https://ecourt-cdn.surepass.io?68a78ed32405fea773896c5ed5d51d2c0211b266882375e2c890821097dcac350f129b51a0335d0163d2f24c3564ec9e"
          }
        ],
        "order_flow": [],
        "petitioner": "Navya Naveli Rai",
        "state_code": "29",
        "dist_code": "0",
        "court_number": "",
        "registration_number": "",
        "filing_number": "",
        "filing_date": "30/07/2021",
        "hearing_date": "",
        "court_number_and_judge": "The Honourable Sri Justice ABHINAND KUMAR SHAVILI",
        "respondent": "The Government of Telangana",
        "case_name": "",
        "case_type_name": "WP(WRIT PETITION)",
        "case_type_number": "",
        "court_name": "High Court of Telangana",
        "case_status": "Pending",
        "case_no": "WP/17906/2021",
        "fir_number": "",
        "fir_link": "",
        "dist": "",
        "police_station": "",
        "circle": "",
        "state": "Telangana",
        "court_type": "High Court",
        "district": "",
        "case_link": "https://csis.tshc.gov.in/",
        "suit_filed_amount": "",
        "gfc_updated_at": "25th May 2023",
        "created_at": "23rd May 2023",
        "cnr_number": "",
        "case_reg_date": "31/07/2021",
        "petitioner_address": "",
        "respondent_address": "",
        "under_act": "",
        "under_section": "",
        "nature_of_disposal": "",
        "gfc_respondents": [
          {
            "name": "The Government of Telangana - Rep by its Principal Secretary Higher Education Secretariat Buildings Hyderabad "
          },
          {
            "name": "The Comissioner - Higher Education for the State of Telangana Vidya Bhavan Nampally Hyderabad "
          },
          {
            "name": "University Grants Commission - Bahadur Shah Zafar Marg New Delhi110002 "
          },
          {
            "name": "South Central Regional Office - All India Counsel for Technical Education Rep by its Regional Officer II Floor Swarna Jayanthi Commercial Complex Ameerpet Hyderabad "
          },
          {
            "name": "Woxsen University - Kamkole Sadasivpet Sangareedy District Telangana502345 "
          }
        ],
        "gfc_petitioners": [
          {
            "name": "Navya Naveli Rai daughterof  Priya Naveen Age Mejor Occ Student",
            "address": "R/o  63166/214 flat no 214 Laxminarayana Villa Shivrampally roads Opp Aramghar and pillar no 321 Hyderabad 500052"
          },
          {
            "name": "Sana Zabeen daughterof  Shaik Jeelani Age Mejor OCC Student R/Hno 3217/18/5/1 plot n no 78 Seetha Ram Nagar Safilguda Hyderabad"
          },
          {
            "name": "Yash Khare sonof  Rajcsh Khare Age Mejor OCC Student",
            "address": "R/o  406 L I G no 8 Circuit house colony Chhatarpur M P  471001"
          },
          {
            "name": "Sathvika Reddy daughterof  Deepika Reddy Age Mejor OCC Student",
            "address": "R/o  H no 1231/7 Brindavan Colony Nizampet Hyderabad  500090"
          },
          {
            "name": "Tadipatri Sharun Babu - S/0 Tadipatri Babu Age Mejor OCC Student R/m Nagar Anantapur Andhrapradesh515004 "
          },
          {
            "name": "Sai Venkat Sathwik Chitturi sonof  Prasanna Srinivas Chitturi Age Mejor OCC Student",
            "address": "R/o  Plot 374 and 375 Flat 304 Park View Residency 6th Phase KPHB Colony 19 Kukkatpally Hyderabad  500072"
          },
          {
            "name": "Vismaya Vineeth daughterof  Vineeth 0 Pamban Age Mejor OCC Student",
            "address": "R/o  5B2 Mithilam Nolambur Chennai TN600095"
          },
          {
            "name": "Pathi Sidhartha sonof  Shylaja Age Mejor OCC Student",
            "address": "R/o  362/d Hemanagar Boduppal Hyderabad"
          },
          {
            "name": "Saikamal sonof  Ramesh Age Mejor OCC Student R/mnagar Street Eturnagaram JayashankarBhoopalpalli District Telangana 506165"
          },
          {
            "name": "Vanditha Gudavalli - D/0 Nageswara Rao Age Mejor OCC Student ",
            "address": "R/o  GI Seven hills apartments Phase 6 KPHB Near KS Bakers Hyderabad"
          },
          {
            "name": "Meghna Patra daughterof  Prasanta Kumar Patra Age Mejor OCC Student R/Gandhi Nagar 2nd lane Shree Ganesh appartments 2nd floor Berhampur Ganjam Odisha 760001"
          },
          {
            "name": "Meghna Boorugu daughterof  Naresh Boorugu Age Mejor OCC Student",
            "address": "R/o  1102/4 Boorugu vihar Lane Beside Andhra Bank Begumpet Hyderabad 500016"
          },
          {
            "name": "Snehal Rahane daughterof  Prakash Rahane Age Mejor OCC Student",
            "address": "R/o  2 Jeevan chaya Jachak mala Jai Bhavani Road Nashik road Maharashtra 422102"
          },
          {
            "name": "Debu daughterof  Selwyn dharma edwards Age Mejor OCC Student",
            "address": "R/o  58/120 Thompson Street Palace Road Nagercoil629001"
          },
          {
            "name": "Krushna Palkritwar daughterof  Prashant Palkriwar Age Mejor OCC Student",
            "address": "R/o  No Above S B formulation Pusad Yavatmal"
          },
          {
            "name": "Yeshaswini M daughterof  Mohan Naidu Age Mejor OCC Student",
            "address": "R/o  1040 MRC Brundavanam BSK 2nd stage 14th cross Near Sri Hari Kalyana Mantapa Bangalore 560070"
          },
          {
            "name": "Nandika Singh Parihar daughterof  Mukut Singh Parihar Age Mejor OCC Student",
            "address": "R/o  1A/7 Vijay nagar Behind police station IndoreMP  452010"
          },
          {
            "name": "Priyamvada Joshi daughterof  Anjali Joshi Age Mejor OCC Student",
            "address": "R/o  AS7 Stone Valley apartments Road no 4 Banjara hills Hyderabad"
          },
          {
            "name": "Nakul Dnyane sonof  Mallikarjun Dayane Age Mejor OCC Student",
            "address": "R/o  103 281 Navipeth Jalgaon Maharashtra"
          },
          {
            "name": "Sonika Yenamandra daughterof  Lakshmi Yenamandra",
            "address": "R/o  49293/1 Padmanagar colony phase1 BH IDPL colony Hyderabad 500037"
          },
          {
            "name": "Harisankar Sugathan - S/0 Sugathan G ",
            "address": "R/o  Madhavam Kakkakuzhy Nellivila P O 19 Thiruvananthapul am 695523"
          },
          {
            "name": "Abhinav Sai Kolla - S/0 K Manikumar ",
            "address": "R/o  Flat 403 7135 and 35/A Shyam Karan road Ameerpet Hyderabad Telangana  500016"
          },
          {
            "name": "Radhe Trivedi - D/0 Mnisha Trivedi ",
            "address": "R/o  706 Vrajbhumi apt Behaind Sanjay apt Vikram sarabhai marg Ambawadi Ahmedabad 380006"
          },
          {
            "name": "Aanya Nangalia daughterof  Sanjeev Nangalia",
            "address": "R/o  J311 jain Carlton creek Khajaguda Hyderabad 500089"
          },
          {
            "name": "Sejal Saxena daughterof  Prabhat Saxena",
            "address": "R/o  E182 01d Minal Residency J K Road Bhopal Pin code462023"
          },
          {
            "name": "Pruthvesh Dongre sonof  Harshada Dongre",
            "address": "R/o  Chaitanya nagar6 Dapoli Ratnagiri Maharashtra 415712"
          },
          {
            "name": "Shlok Bhutada - S/njay Bhutada ",
            "address": "R/o  7163/5 DK road Ameerpet Hyderabad"
          },
          {
            "name": "Kaaviya subramaniam daughterof  Mallika Subrannaniam",
            "address": "R/o  25/139 EL Behind murugan koil Salem road Namakkal 20 Tamilnadu"
          },
          {
            "name": "M Sathwik reddy - S/0 M Padma Reddy R/I 41/2 Shankar nagar Chandanagar Hyderabad "
          }
        ],
        "gfc_fir_respondents": [],
        "gfc_fir_petitioners": [],
        "case_details_link": "https://ecourt-cdn.surepass.io?gfcId=d775bfce61f5a85e67a87159c5ba72f01bb89c0000412058ba9040553894552dbd785d5c228b16ea461998c28b5f5af6",
        "gfc_fir_number_court": "",
        "gfc_fir_year_court": "",
        "gfc_fir_policestation_court": "",
        "gfc_orders_data": {
          "petitioners": [],
          "respondents": []
        },
        "case_type": ""
      }
    ]
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Thu, 13 Jun 2024 06:04:51 GMT

Content-Type

application/json

Content-Length

50060

Connection

keep-alive

## 

UAE

Request Group for UAE ID verification requests.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### GETDistrict List

https://kyc-api.surepass.io/api/v1/land-verification/gujarat/meta/district-list

This API provides a list of districts in Gujarat for land verification.

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/land-verification/gujarat/meta/district-list' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": [
    "ahmadabad",
    "amreli",
    "anand",
    "arvalli",
    "banaskantha",
    "bharuch",
    "bhavnagar",
    "botad",
    "chhotaudepur",
    "dahod",
    "dangs",
    "devbhumi dwarka",
    "gandhinagar",
    "gir somnath",
    "jamnagar",
    "junagadh",
    "kachchh",
    "kheda",
    "mahesana",
    "mahisagar",
    "morbi",
    "narmada",
    "navsari",
    "panchmahals",
    "patan",
    "porbandar",
    "rajkot",
    "sabarkantha",
    "surat",
    "surendranagar",
    "tapi",
    "vadodara",
    "valsad"
  ],
  "status_code": 200,
  "message_code": "success",
  "message": "Success",
  "success": true
}
```

Date

Tue, 28 Jan 2025 12:27:12 GMT

Content-Type

application/json

Content-Length

489

Connection

keep-alive

### POSTTaluka List

https://kyc-api.surepass.io/api/v1/land-verification/gujarat/meta/taluka-list

This API takes the **district name** as input and returns a list of taluka within the specified district of Gujarat for Land Verification.

**Request Body**

Key

Type

Description

district

String

Name of the district

**Response Body**

Key

Type

Description

district\_name

String

Name of the district

taluka\_list

List of String

List of talukas within the district

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "district": "sabarkantha"
}
```

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/land-verification/gujarat/meta/taluka-list' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "district": "sabarkantha"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "district_name": "sabarkantha",
    "taluka_list": [
      "khedbrahma",
      "vijaynagar",
      "vadali",
      "idar",
      "himatnagar",
      "prantij",
      "talod",
      "poshina"
    ]
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Tue, 28 Jan 2025 12:30:18 GMT

Content-Type

application/json

Content-Length

237

Connection

keep-alive

### POSTGSTIN To MCC

https://kyc-api.surepass.io/api/v1/mcc-mapping/gstin-to-mcc

This API maps a given GSTIN to relevant MCC codes for both goods and services. It provides classification details, confidence levels, and justifications based on related HSN codes.

**Request Body**

Key

Format

Description

gstin

String

GST Identification Number

**Response Body**

Key

Format

Description

client\_id

String

Unique client ID

gstin

String

GST Identification Number

goods

List of Object

List of goods classified under HSN

services

List of Object

List of mapped services with MCC codes and details

**goods (Object)**

Key

Format

Description

mcc\_code

String

Merchant Category Code

justification

String

Explanation of why the service maps to the given MCC

confidence

String

Confidence level of the mapping

related\_hsn

List

List of related HSN codes

**services (Object)**

Key

Format

Description

mcc\_code

String

Merchant Category Code

justification

String

Explanation of why the service maps to the given MCC

confidence

String

Confidence level of the mapping

related\_hsn

List

List of related HSN codes

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

HEADERS

Content-Type

application/json

Bodyraw (json)

json

```json
{
    "gstin": "32ABCPU7961K1YY"
}
```

Example Request

Success

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/mcc-mapping/gstin-to-mcc' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "gstin": "32ABCPU7961K1YY"
}'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "gstin_to_mcc_kpiYdmkbOngxYStvuixb",
    "gstin": "32ABCPU7961K1YY",
    "goods": [
      {
        "mcc_code": "5311",
        "justification": "Retail business generally falls under department stores if selling a variety of goods. This is a common MCC for general retail.",
        "confidence": "High",
        "related_hsn": [
          "4202",
          "4203",
          "4205"
        ]
      },
      {
        "mcc_code": "5941",
        "justification": "Sporting Goods Stores are common retail outlets. HSN codes related to sporting goods are relevant.",
        "confidence": "Medium",
        "related_hsn": [
          "9506",
          "9507"
        ]
      }
    ],
    "services": [
      {
        "mcc_code": "7299",
        "justification": "This MCC covers miscellaneous services not elsewhere classified, which could be relevant for a retail business offering minor services.",
        "confidence": "Low",
        "related_hsn": [
          "9985",
          "9986"
        ]
      }
    ]
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Thu, 20 Mar 2025 12:08:04 GMT

Content-Type

application/json

Content-Length

863

Connection

keep-alive

## 

PDF Metadata Check

This API extracts metadata from a PDF, like file size, PDF version, title, author, creation and modification dates, encryption status, risk level, and warnings to check if the document was modified or manipulated.

AUTHORIZATIONBearer Token

This folder is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

### POSTPDF Metadata Check

https://kyc-api.surepass.io/api/v1/pdf-metadata-check/upload

**Request Body**

**Key**

**Format**

**Description**

file

PDF

Upload PDF

**Response Body**

View More

Key

Format

Description

client\_id

String

Unique identifier for the PDF metadata check request

file\_size

String

Size of the PDF file in kilobytes

pdf\_version

String

PDF version of the uploaded file

title

String

Title metadata of the PDF

author

String

Author metadata of the PDF

creator

String

Application or tool used to create the PDF

producer

String

Software that produced the PDF

creation\_date

String

Date and time when the PDF was created

modification\_date

String

Date and time when the PDF was last modified

is\_encrypted

Boolean

Indicates if the PDF is password protected or encrypted

risk\_level

String

Overall risk level detected for the PDF

warnings

List of Object

List of warnings related to the PDF file

**warnings (Object)**

Key

Format

Description

indicator\_id

String

Warning type identifier

description

String

Warning message details

AUTHORIZATIONBearer Token

This request is using Bearer Token from collection[Surepass API](#auth-info-942d8ae1-75fa-4c6a-a2e5-8c54a74107ae)

Bodyformdata

file

Example Request

Success

View More

curl

```curl
curl --location 'https://kyc-api.surepass.io/api/v1/pdf-metadata-check/upload' \
--header 'Authorization: Bearer TOKEN' \
--form 'file=@"/Users/karanjeetsingh/Downloads/pdf_metadata/Bank_Scan240526030834_1365743103.pdf"'
```

200 OK

Example Response

-   Body
-   Headers (4)

View More

json

```json
{
  "data": {
    "client_id": "pdf_metadata_check_coaqdGbHeOvdmUdjfpLR",
    "file_size": "656.83",
    "pdf_version": "1.4",
    "title": "",
    "author": "",
    "creator": "",
    "producer": "iText® 5.5.10 ©2000-2015 iText Group NV (AGPL-version)",
    "creation_date": "2021-04-08T12:04:40",
    "modification_date": "2021-04-08T12:07:03",
    "is_encrypted": false,
    "risk_level": "high",
    "warnings": [
      {
        "indicator_id": "modified_metadata",
        "description": "This document was modified after it was created. This could be a sign of manipulation with a PDF editor"
      },
      {
        "indicator_id": "modified_document",
        "description": "This document has been incrementally updated. This is highly atypical for this type of document. This document is likely manipulated"
      }
    ]
  },
  "status_code": 200,
  "success": true,
  "message": "Success",
  "message_code": "success"
}
```

Date

Tue, 22 Apr 2025 12:29:51 GMT

Content-Type

application/json

Content-Length

451

Connection

keep-alive