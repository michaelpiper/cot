from collections import abc
from ...domain.models.context import AsyncContext
import json
import re
from ..logger import logger
class EntityContext(AsyncContext): 
    async def generate_text(self, user_input = []) -> str:
        system_prompt = await self.get_system_prompt()
        logger.info("System Input: {}".format(system_prompt))
        # Combine the system prompt and user input
        prompt  =   [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": system_prompt}, 
                    ]
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_input},]
                },
            ]
        
        # Generate the response
        response = await self.generator.generate(
            prompt,
            max_new_tokens=1200,
            # truncation=True,
            num_return_sequences=1,
            temperature=0.7  # Adjust for creativity vs. determinism
        )
       
        if isinstance(response,abc.Generator):
            generated_text = ""
            for output in response:
                generated_text += output
        else:
            generated_text = response     
        logger.info("Generated Text: {}".format(generated_text))
        # Clean up the generated text to ensure valid JSON
        try:
            # Extract the generated text
            # Use regex to extract the JSON part from the generated text
            json_match = re.search(r"\{.*\}", generated_text, re.DOTALL)
            if json_match:
                generated_text = json_match.group(0)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            generated_text = "{}"
        return generated_text
    
    async def get_system_prompt(self) -> str:
        """
        Generate a system prompt based on the current context.
        """
        system_prompt = f"""
        You are an intelligent assistant designed to extract valuable information from user input. Your task is to identify and extract the following details from the user's message:
        --- 
            ### **1. Personal Identification Entities**
            - **First name**  
            - **Last name**  
            - **Full name**  
            - **Date of birth**  
            - **National ID number**  
            - **Passport number**  
            - **Tax ID (e.g., SSN, TIN)**  
            - **Biometric data** (fingerprint, facial recognition)  

            ---

            ### **2. Contact Information Entities**
            - **Email address**  
            - **Phone number**  
            - **Residential address** (street, city, state, postal code)  
            - **Mailing address** (if different)  
            - **Preferred language**  

            ---

            ### **3. Account & Transaction Entities**
            - **Account number**  
            - **Account type** (savings, checking, fixed deposit, etc.)  
            - **Card number** (debit/credit)  
            - **Transaction ID**  
            - **Transaction amount**  
            - **Transaction date/time**  
            - **Transaction description**  
            - **Beneficiary name**  
            - **Beneficiary account number**  
            - **Transfer reference number**  

            ---

            ### **4. Financial Entities**
            - **Balance amount**  
            - **Loan amount**  
            - **Interest rate**  
            - **Loan term** (duration)  
            - **Minimum balance requirement**  
            - **Fee amount** (e.g., transfer fees, dormancy fees)  
            - **Exchange rate** (for forex transactions)  

            ---

            ### **5. Document & Verification Entities**
            - **Document type** (e.g., passport, driver’s license, utility bill)  
            - **Document number**  
            - **Document expiry date**  
            - **KYC status** (verified/unverified)  
            - **Signature image**  

            ---

            ### **6. Location-Based Entities**
            - **ATM location**  
            - **Branch address**  
            - **Banking agent location**  
            - **Country/Currency** (for international transfers)  

            ---

            ### **7. Temporal Entities**
            - **Date/Time** (e.g., statement period, loan disbursement date)  
            - **Dormancy period** (e.g., "6 months")  
            - **Validity period** (e.g., data bundle expiry)  

            ---

            ### **8. Service-Specific Entities**
            - **Complaint reference number**  
            - **Loan application ID**  
            - **Bill payment reference**  
            - **Airtime recipient number**  
            - **Data plan name** (e.g., "1GB weekly bundle")  
            - **Bill type** (electricity, water, cable TV)  
            - **Biller name**  

            ---

            ### **9. Security & Authentication Entities**
            - **PIN** (for cards/apps)  
            - **Password** (online banking)  
            - **Security question/answer**  
            - **One-time password (OTP)**  
            - **Device ID** (for app authorization)  

            ---

            ### **10. Status & Categorical Entities**
            - **Account status** (active/dormant/blocked)  
            - **Card status** (lost/stolen/blocked)  
            - **Complaint category** (fraud, service quality)  
            - **Delivery method** (e-statement, postal mail)  
            - **Notification preference** (SMS/email/push)  
        ---

        If a piece of information is not explicitly provided in the user's message, you MUST respond with "N/A". Do not infer or guess any values that are not explicitly stated. Always format your response as a JSON object with the following structure:
        {json.dumps({
        "personal_identification": {
            "first_name": "value",
            "last_name": "value",
            "full_name": "value",
            "date_of_birth": "value",
            "national_id": "value",
            "passport_number": "value",
            "tax_id": "value"
        },
        "contact_information": {
            "email": "value",
            "phone_number": "value",
            "residential_address": "value",
            "mailing_address": "value",
            "preferred_language": "value"
        },
        "account_details": {
            "account_number": "value",
            "account_type": "value",
            "card_number": "value",
            "transaction_id": "value",
            "balance": "value",
            "transaction_amount": "value",
            "transaction_date": "value"
        },
        "financial_entities": {
            "loan_amount": "value",
            "interest_rate": "value",
            "minimum_balance": "value",
            "fee_amount": "value",
            "exchange_rate": "value"
        },
        "verification_documents": {
            "document_type": "value",
            "document_number": "value",
            "expiry_date": "value",
            "kyc_status": "value"
        },
        "location_data": {
            "atm_location": "value",
            "branch_address": "value",
            "country": "value",
            "currency": "value"
        },
        "temporal_data": {
            "date_time": "value",
            "dormancy_period": "value",
            "validity_period": "value"
        },
        "service_metadata": {
            "complaint_id": "value",
            "loan_application_id": "value",
            "bill_reference": "value",
            "data_plan": "value"
        },
        "security_credentials": {
            "pin": "value",
            "password": "value",
            "otp": "value",
            "device_id": "value"
        },
        "status_flags": {
            "account_status": "value",
            "card_status": "value",
            "complaint_category": "value",
            "delivery_method": "value"
        },
        "notes": "value",
        "preferred_lang": "value",
        }, indent=2)
        }

        IMPORTANT:
        - Do not infer or guess any values that are not explicitly provided by the user.
        - If a piece of information is missing, you MUST use "N/A".
        - Be precise and ensure the extracted information is accurate.    
        - only output the JSON string 
        """ 
        return system_prompt