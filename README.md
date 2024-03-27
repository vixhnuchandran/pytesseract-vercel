# Pytesseract Vercel OCR API

## Description

This API provides Optical Character Recognition (OCR) functionality using the Pytesseract library deployed on Vercel. It accepts images either as base64-encoded strings or as file uploads and returns the recognized text along with bounding box coordinates for each recognized word.

## Endpoints

### Base URL

The base URL for this API is: https://your-vercel-deployment-url/api/ocr

### `/api/ocr` - POST

#### Description

This endpoint accepts an image either as a base64-encoded string or as a file upload and performs OCR on it.

#### Request

- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json` for JSON body, or form data for file uploads.
- **Body**:
  - For JSON body:
    ```json
    {
        "image": "base64_encoded_image_string"
    }
    ```
  - For file upload:
    Form data with key `image` containing the image file.

#### Response

- **Status Code**: 200 OK
- **Body**:
  ```json
  {
      "text": "Recognized text from the image",
      "bboxes": [
          {
              "text": "word",
              "data": {
                  "confidence": 0.95,
                  "bbox": {
                      "left": 10,
                      "top": 20,
                      "right": 50,
                      "bottom": 30
                  }
              }
          },
          ...
      ]
  }
## Errors

- **Status Code**: 400 Bad Request
  - If image data is not provided.
- **Status Code**: 415 Unsupported Media Type
  - If the request content type is not supported.
- **Status Code**: 500 Internal Server Error
  - For any other errors during OCR processing.

## Notes

- This API is deployed on Vercel, and currently, Vercel does support setting up runtime binaries.
- However, due to the limitations of the Vercel runtime environment, there might be issues with installing dependencies such as Tesseract-OCR, which is required for Pytesseract to function properly.
- Ensure proper configuration of the runtime environment to include necessary dependencies like Tesseract-OCR (`tesseract-ocr`) for optimal performance.
- Consider alternative deployment options if dependencies cannot be properly configured within the Vercel environment.

